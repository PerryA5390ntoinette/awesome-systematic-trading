# Asset Growth Effect Strategy
# Based on: Cooper, Gulen, and Schill (2008)
# "Asset Growth and the Cross-Section of Stock Returns"
#
# Strategy Logic:
# - Firms with low asset growth rates earn higher future returns than firms with high asset growth rates
# - Go long on stocks with lowest total asset growth (bottom decile)
# - Go short on stocks with highest total asset growth (top decile)
# - Rebalance annually

from AlgorithmImports import *
from datetime import timedelta


class AssetGrowthEffect(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(1_000_000)

        self.SetSecurityInitializer(
            lambda x: x.SetFeeModel(ConstantFeeModel(0))
        )

        self.coarse_count = 1000
        self.long_count = 50
        self.short_count = 50
        self.rebalance_months = 12
        self.last_rebalance = datetime.min

        self.long_symbols = []
        self.short_symbols = []
        self.filtered_fine = None

        self.AddUniverse(
            self.CoarseSelectionFunction,
            self.FineSelectionFunction
        )

        self.Schedule.On(
            self.DateRules.MonthStart(),
            self.TimeRules.AfterMarketOpen("SPY", 30),
            self.Rebalance
        )

        self.AddEquity("SPY", Resolution.Daily)

    def CoarseSelectionFunction(self, coarse):
        # Filter by price and volume, require fundamental data
        filtered = [
            x for x in coarse
            if x.HasFundamentalData
            and x.Price > 5
            and x.DollarVolume > 1_000_000
        ]

        # Sort by dollar volume and take top N
        sorted_by_volume = sorted(
            filtered,
            key=lambda x: x.DollarVolume,
            reverse=True
        )

        return [x.Symbol for x in sorted_by_volume[:self.coarse_count]]

    def FineSelectionFunction(self, fine):
        # Filter to those with valid total assets data for two consecutive years
        valid = [
            x for x in fine
            if x.FinancialStatements.BalanceSheet.TotalAssets.TwelveMonths > 0
            and x.FinancialStatements.BalanceSheet.TotalAssets.OneYear > 0
        ]

        # Calculate asset growth rate: (Total Assets[t] - Total Assets[t-1]) / Total Assets[t-1]
        for stock in valid:
            current_assets = stock.FinancialStatements.BalanceSheet.TotalAssets.TwelveMonths
            prior_assets = stock.FinancialStatements.BalanceSheet.TotalAssets.OneYear
            stock.AssetGrowth = (current_assets - prior_assets) / prior_assets

        # Sort by asset growth rate
        sorted_by_growth = sorted(valid, key=lambda x: x.AssetGrowth)

        # Bottom decile (lowest growth) -> long
        self.long_symbols = [
            x.Symbol for x in sorted_by_growth[:self.long_count]
        ]
        # Top decile (highest growth) -> short
        self.short_symbols = [
            x.Symbol for x in sorted_by_growth[-self.short_count:]
        ]

        return self.long_symbols + self.short_symbols

    def OnSecuritiesChanged(self, changes):
        # Liquidate removed securities
        for security in changes.RemovedSecurities:
            if security.Invested:
                self.Liquidate(security.Symbol)

    def Rebalance(self):
        # Only rebalance once per year
        if (self.Time - self.last_rebalance).days < 30 * self.rebalance_months:
            return

        if not self.long_symbols or not self.short_symbols:
            return

        self.last_rebalance = self.Time

        # Liquidate positions not in current universe
        current_targets = set(self.long_symbols + self.short_symbols)
        for symbol, holding in self.Portfolio.items():
            if holding.Invested and symbol not in current_targets:
                self.Liquidate(symbol)

        # Equal weight allocation
        long_weight = 0.5 / len(self.long_symbols)
        short_weight = -0.5 / len(self.short_symbols)

        # Enter long positions (low asset growth)
        for symbol in self.long_symbols:
            self.SetHoldings(symbol, long_weight)

        # Enter short positions (high asset growth)
        for symbol in self.short_symbols:
            self.SetHoldings(symbol, short_weight)

        self.Log(
            f"Rebalanced: {len(self.long_symbols)} long, "
            f"{len(self.short_symbols)} short at {self.Time}"
        )

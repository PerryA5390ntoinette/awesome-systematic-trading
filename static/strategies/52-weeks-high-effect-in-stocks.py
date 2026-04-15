# https://quantpedia.com/strategies/52-weeks-high-effect-in-stocks/
#
# The investment universe consists of all stocks from NYSE, AMEX and NASDAQ (the research paper used the CRSP 
# database for backtesting). The ratio between the current price and 52-week high is calculated for each stock 
# at the end of each month (PRILAG i,t = Price i,t / 52-Week High i,t). Every month, the investor then calculates
# the weighted average of ratios (PRILAG i,t) from all firms in each industry (20 industries are used), where the
# weight is the market capitalization of the stock at the end of month t. The winners (losers) are stocks in the
# six industries with the highest (lowest) weighted averages of PRILAGi,t. The investor buys stocks in the winner
# portfolio and shorts stocks in the loser portfolio and holds them for three months. Stocks are weighted equally
# and the portfolio is rebalanced monthly (which means that 1/3 of the portfolio is rebalanced each month).
#
# QC implementation changes:
#   - Universe consists of 500 most liquid stocks traded on NYSE, AMEX, or NASDAQ.
#
# Personal notes:
#   - Reduced coarse_count to 300 to speed up backtesting during development; bump back to 500 for final runs.
#   - Started backtest from 2010 to focus on more recent market regimes.

from numpy import floor
from AlgorithmImports import *

class Weeks52HighEffectinStocks(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  # Changed from 2000 to 2010 for faster iteration
        self.SetCash(100000)

        self.SetSecurityInitializer(lambda x: x.SetMarketPrice(self.GetLastKnownPrice(x)))
        
        self.period = 12 * 21

        # Tranching.
        self.holding_period = 3
        self.managed_queue = []

        # Daily 'high' data.
        self.data = {}
        
        self.symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        
        self.coarse_count = 300  # Reduced from 500 for faster dev backtests
        self.selection_flag = False
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        self.Schedule.On(self.DateRules.MonthEnd(self.symbol), self.TimeRules.AfterMarketOpen(self.symbol), self.Selection)

    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.SetFeeModel(CustomFeeModel())
            security.SetLeverage(10)
            
    def CoarseSelectionFunction(self, coarse):
        # Update the rolling window every day.
        for stock in coarse:
            symbol = stock.Symbol

            if symbol in self.data:
                # Store daily price.
                self.data[symbol].update(stock.AdjustedPrice)
            
        if not self.selection_flag:
            return Universe.Unchanged
        
        selected = [x.Symbol
            for x in sorted([x for x in coarse if x.HasFundamentalData and x.Market == 'usa'],
                key = lambda x: x.DollarVolume, reverse = True)[:self.coarse_count]]
        
        # Warmup price rolling windows.
        for symbol in selected:
            if symbol in self.data:
                continue
            
            self.data[symbol] = SymbolData(symbol, self.period)
            his

# https://quantpedia.com/strategies/12-month-cycle-in-cross-section-of-stocks-returns/
#
# The top 30% of firms based on their market cap from NYSE and AMEX are part of the investment universe. Every month, stocks are grouped 
# into ten portfolios (with an equal number of stocks in each portfolio) according to their performance in one month one year ago. Investors
# go long in stocks from the winner decile and shorts stocks from the loser decile. The portfolio is equally weighted and rebalanced every month.
#
# QC implementation changes:
#   - Universe consists of top 3000 US stock by market cap from NYSE, AMEX and NASDAQ.
#   - Portfolio is value weighted.
#
# Personal notes:
#   - Increased coarse_count from 500 to 1000 for a broader universe sample.
#   - The original paper uses top 30% by market cap; using dollar volume as proxy here.

from AlgorithmImports import *

class Month12CycleinCrossSectionofStocksReturns(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2000, 1, 1)  
        self.SetCash(100000)

        self.symbol = self.AddEquity('SPY', Resolution.Daily).Symbol
        
        # Increased from 500 to 1000 to capture a wider universe
        self.coarse_count = 1000
        
        # Monthly close data.
        self.data = {}
        self.period = 13
        
        self.weight = {}

        self.selection_flag = False
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)
        
        self.Schedule.On(self.DateRules.MonthEnd(self.symbol), self.TimeRules.BeforeMarketClose(self.symbol), self.Selection)

    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            security.SetFeeModel(CustomFeeModel())
            security.SetLeverage(10)
            
    def CoarseSelectionFunction(self, coarse):
        if not self.selection_flag:
            return Universe.Unchanged

        # Update the rolling window every month.
        for stock in coarse:
            symbol = stock.Symbol

            # Store monthly price.
            if symbol in self.data:
                self.data[symbol].update(stock.AdjustedPrice)

        # selected = [x.Symbol for x in coarse if x.HasFundamentalData and x.Market == 'usa']
        selected = [x.Symbol
            for x in sorted([x for x in coarse if x.HasFundamentalData and x.Market == 'usa'],
                key = lambda x: x.DollarVolume, reverse = True)[:self.coarse_count]]
        
        # Warmup price rolling windows.
        for symbol in selected:
            if symbol in self.data:
                continue
            
            self.data[symbol] = SymbolData(symbol, self.period)
            history = self.History(symbol, self.period*30, Resolution.Daily)
            if history.empty:
                self.Log(f"Not enough data for {symbol} yet.")
                continue
            closes = history.loc[symbol].close
            
            closes_len = len(closes.keys())
            # Find monthly closes.
            for index, time_close in enumerate(closes.iteritems()):
                # index out of bounds check.
                if index + 1 < closes_len:
                   
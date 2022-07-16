from datetime import datetime
import backtrader as bt
from pandas_datareader import data as pddata
import pandas as pd


# pip install pandas_datareader for yahoo data


# Create a subclass of Strategy to define the indicators and logic

class SmaCross(bt.Strategy):
    """Doc."""
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


# get data
codes = ['aapl', 'ibm', 'msft', 'goog']  # 四个股票

all_stock = {}

for ticker in codes:
    all_stock[ticker] = pddata.get_data_yahoo(ticker, start='1/1/2018', end='30/3/2018')  # 默认从2010年1月起始

print(all_stock['msft'])


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

# Create a data feed
data = bt.feeds.PandasData(all_stock['msft'])
# data = bt.feeds.YahooFinanceData(dataname='MSFT',
#                                  fromdate=datetime(2011, 1, 1),
#                                  todate=datetime(2012, 12, 31))

cerebro.adddata(data)  # Add the data feed

cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.run()  # run it all
# cerebro.plot()

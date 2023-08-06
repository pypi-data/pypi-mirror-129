#####
# Used to load local lumibot folder into a venv
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")
#####

import logging
from datetime import datetime, timedelta
from time import time

import pandas as pd
from strategies.diversified_leverage import DiversifiedLeverage
from strategies.ml_strategy import MachineLearning
from strategies.nic_strategy import NicBot
from twilio.rest import Client

from credentials import AlpacaConfig, InteractiveBrokersConfig, TwilioConfig
from lumibot.backtesting import (
    AlpacaBacktesting,
    AlphaVantageBacktesting,
    BacktestingBroker,
    PandasDataBacktesting,
    YahooDataBacktesting,
)
from lumibot.brokers import Alpaca, InteractiveBrokers
from lumibot.data_sources import PandasData
from lumibot.tools import indicators
from lumibot.traders import Trader

# Choose your budget and log file locations
budget = 50000
logfile = "logs/test.log"
benchmark_asset = None

# Initialize all our classes
trader = Trader(logfile=logfile)

# Development: Minute Data
asset = "SRNE"
df = pd.read_csv(f"data/{asset}_Minute.csv")
df = df.set_index("time")
df.index = pd.to_datetime(df.index)
my_data = dict()
my_data[asset] = df
backtesting_start = datetime(2021, 8, 8)
backtesting_end = datetime(2021, 8, 15)

####
# Select our strategy
####

pandas = PandasData(my_data)
broker = BacktestingBroker(pandas)

strategy_name = "DiversifiedLeverage"

####
# Backtest
####

# MachineLearning.backtest(
#     strategy_name,
#     budget,
#     PandasDataBacktesting,
#     backtesting_start,
#     backtesting_end,
#     config=AlpacaConfig,
#     pandas_data=my_data,
#     symbol=asset,
# )

####
# Run the strategy
####

broker = Alpaca(AlpacaConfig)
strategy = DiversifiedLeverage(
    name=strategy_name,
    budget=budget,
    broker=broker,
)
trader.add_strategy(strategy)
trader.run_all()

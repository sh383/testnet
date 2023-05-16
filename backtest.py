from binance import Client
import numpy as np
import pandas as pd
from datetime import datetime


api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

symbol = "BTCUSDT"  # Example: Bitcoin symbol
interval = Client.KLINE_INTERVAL_1HOUR  # Example: 1-hour interval

start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 5, 15)

klines = client.get_historical_klines(
    symbol,
    interval,
    start_date.strftime("%d %b %Y %H:%M:%S"),
    end_date.strftime("%d %b %Y %H:%M:%S"),
)

df = pd.DataFrame(
    klines,
    columns=[
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ],
)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

df["range"] = (df["high"] - df["low"]) * 0.5
df["target"] = df["open"] + df["range"].shift(1)

fee = 0.0032
df["ror"] = np.where(df["high"] > df["target"], df["close"] / df["target"] - fee, 1)

df["hpr"] = df["ror"].cumprod()
df["dd"] = (df["hpr"].cummax() - df["hpr"]) / df["hpr"].cummax() * 100
print("MDD(%): ", df["dd"].max())
df.to_csv("dd.csv")

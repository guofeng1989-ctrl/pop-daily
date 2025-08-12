import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

def score(df, tech_now):
    rsi = RSIIndicator(df["Close"]).rsi().iloc[-1]
    macd = MACD(df["Close"])
    macd_diff = macd.macd_diff().iloc[-1]
    bb = BollingerBands(df["Close"])
    bb_pos = (df["Close"].iloc[-1] - bb.bollinger_l().iloc[-1]) / (bb.bollinger_h().iloc[-1] - bb.bollinger_l().iloc[-1])

    score_val = 50
    if rsi < 30: score_val += 15
    elif rsi > 70: score_val -= 15
    if macd_diff > 0: score_val += 10
    else: score_val -= 10
    if bb_pos < 0.2: score_val += 10
    elif bb_pos > 0.8: score_val -= 10
    return min(100, max(0, int(score_val)))

if __name__ == "__main__":
    df = pd.read_csv("history.csv", index_col=0, parse_dates=True)
    from fetch import get_today_tech
    print(score(df, get_today_tech()))

import pandas as pd, requests, datetime as dt, pytz, io, time

TICKER = "09922"   # Tushare 港股代码前加 0
TZ = pytz.timezone("Asia/Hong_Kong")

def get_history(days=730):
    end = dt.datetime.now(TZ)
    start = end - pd.Timedelta(days=days)
    # 用新浪港股历史接口（无需 key，直接返回 csv）
    url = (
        "https://quotes.sina.cn/cn/api/jsonp_v2.php/"
        f"var%20_hk{TICKER}=/HK_MarketDataService.getKLineData"
        f"?symbol=hk{TICKER}&scale=240&ma=no&datalen={days}"
    )
    headers = {"User-Agent": "Mozilla/5.0"}
    txt = requests.get(url, headers=headers, timeout=15).text
    # 去掉 jsonp 外壳，拿到纯 json
    json_str = txt[txt.find("[") : txt.rfind("]") + 1]
    df = pd.read_json(json_str)
    df.rename(columns={"day": "Date", "open": "Open", "high": "High",
                       "low": "Low", "close": "Close", "volume": "Volume"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df = df.loc[start:end]
    df.to_csv("history.csv")
    return df

def get_today_tech():
    # 备用：从新浪实时行情抓 RSI/MACD 太麻烦，这里先给占位值
    return {"RSI": 50, "MACD": 0}

if __name__ == "__main__":
    get_history()

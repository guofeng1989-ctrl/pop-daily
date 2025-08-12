import pandas as pd, requests, datetime as dt, pytz

TICKER = "09922"          # 腾讯/港股泡泡玛特
TZ   = pytz.timezone("Asia/Hong_Kong")

def get_history(days=730):
    end = dt.datetime.now(TZ)
    start = end - pd.Timedelta(days=days)
    # 腾讯行情接口：直接返回 json
    url = (
        "https://web.ifzq.gtimg.cn/appstock/app/HkFq/get"
        f"?code=hk{TICKER}&start={start.strftime('%Y%m%d')}"
        f"&end={end.strftime('%Y%m%d')}"
    )
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers, timeout=15).json()
    # 解析
    kline = data["data"][f"hk{TICKER}"]["day"]
    df = pd.DataFrame(kline, columns=["Date", "Open", "Close", "High", "Low", "Volume", "_1", "_2"])
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df = df.astype(float)
    df.to_csv("history.csv")
    return df

def get_today_tech():
    return {"RSI": 50, "MACD": 0}   # 占位，后面可再优化

if __name__ == "__main__":
    get_history()

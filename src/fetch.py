import pandas as pd, requests, io, datetime as dt, pytz

TICKER = "09922"
TZ = pytz.timezone("Asia/Hong_Kong")

def get_history(days=730):
    # 我已准备好的历史数据（2020-01-01 至今）
    url = "https://gitee.com/limccn/pop-daily-data/raw/master/09922_daily.csv"
    csv = requests.get(url, timeout=15).text
    df = pd.read_csv(io.StringIO(csv), parse_dates=["date"])
df.rename(columns={"date": "Date"}, inplace=True)
    df.set_index("Date", inplace=True)
    # 按日期裁剪
    end = dt.datetime.now(TZ)
    start = end - pd.Timedelta(days=days)
    df = df.loc[start:end]
    df.to_csv("history.csv")
    return df

def get_today_tech():
    return {"RSI": 50, "MACD": 0}   # 占位，后续可扩展

if __name__ == "__main__":
    get_history()

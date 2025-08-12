import yfinance as yf, pandas as pd, requests, datetime as dt, pytz
TICKER = "9992.HK"
TZ = pytz.timezone("Asia/Hong_Kong")

def get_history(days=730):
    end = dt.datetime.now(TZ)
    start = end - pd.Timedelta(days=days)
    df = yf.download(TICKER, start=start, end=end, interval="1d", auto_adjust=True)
    df.dropna(inplace=True)
    df.to_csv("history.csv")
    return df

def get_today_tech():
    url = "https://cn.investing.com/equities/pop-mart-international-group-technical"
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers, timeout=10).text
    import re
    try:
        rsi = float(re.search(r'RSI\(14\)</span></td><td class=".*?>([\d.]+)', html).group(1))
        macd = float(re.search(r'MACD\(12,26\)</span></td><td class=".*?>([\d.-]+)', html).group(1))
    except:
        rsi, macd = 50, 0
    return {"RSI": rsi, "MACD": macd}

if __name__ == "__main__":
    get_history()

import os, datetime as dt, requests, json
from fetch import get_history, get_today_tech
from strategy import score
from model import predict_today

df = get_history()
tech = get_today_tech()
score_val = score(df, tech)
pred = predict_today(df)

msg = f"""【泡泡玛特 每日投资速递】{dt.datetime.now():%Y-%m-%d}
技术面：RSI={tech['RSI']:.1f}  MACD={tech['MACD']:.2f}
量化评分：{score_val}/100
模型预测未来5日收益：{(pred*100):+.2f}%
今日建议：{['谨慎减仓','观望','逢低吸纳'][min(2,int(score_val//40))]}
"""

webhook = os.getenv("WECHAT_WEBHOOK")
if webhook:
    requests.post(webhook, json={"msgtype": "text", "text": {"content": msg}}, timeout=10)
print(msg)

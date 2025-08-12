# PopMartDaily  
每天早上 8:00 自动抓取泡泡玛特（09992.HK）行情并发送投资建议到微信群。

## 使用步骤
1. 把本仓库 fork 到自己名下。  
2. Settings → Secrets → New repository secret → Name 填 `WECHAT_WEBHOOK`，Value 填企业微信群机器人的 webhook 地址。  
3. Actions → PopMartDaily → Run workflow → 立即测试。  
4. 成功后每天 8:00 自动推送。

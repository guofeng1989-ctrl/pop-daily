import pandas as pd, xgboost as xgb, pickle, os
from sklearn.model_selection import train_test_split

def train(df):
    df["ret5"] = df["Close"].shift(-5) / df["Close"] - 1
    df.dropna(inplace=True)
    feats = ["Close", "Volume", "High", "Low"]
    for win in [5, 10, 20]:
        df[f"ma{win}"] = df["Close"].rolling(win).mean()
        df[f"vol{win}"] = df["Close"].pct_change().rolling(win).std()
    df.dropna(inplace=True)
    X = df[feats + [c for c in df.columns if c.startswith("ma") or c.startswith("vol")]]
    y = df["ret5"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    reg = xgb.XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.05)
    reg.fit(X_train, y_train)
    pickle.dump(reg, open("xgb.pkl", "wb"))
    return reg

def predict_today(df):
    if not os.path.exists("xgb.pkl"):
        train(df)
    reg = pickle.load(open("xgb.pkl", "rb"))
    feats = reg.feature_names_in_
    latest = df.iloc[-1:][feats]
    pred = float(reg.predict(latest)[0])
    return pred

if __name__ == "__main__":
    df = pd.read_csv("history.csv", index_col=0, parse_dates=True)
    print(predict_today(df))

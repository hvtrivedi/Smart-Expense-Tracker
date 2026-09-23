import pandas as pd

def summary(df):
    total = float(df["amount"].sum())
    days = max((df["date"].max() - df["date"].min()).days + 1, 1)
    return {
        "total_spending": total,
        "transactions": int(len(df)),
        "average_transaction": float(df["amount"].mean()),
        "average_daily": total / days,
        "highest_transaction": float(df["amount"].max())
    }

def category_summary(df):
    return (df.groupby("category", as_index=False)["amount"]
              .sum().sort_values("amount", ascending=False))

def payment_summary(df):
    return (df.groupby("payment_method", as_index=False)["amount"]
              .sum().sort_values("amount", ascending=False))

def daily_summary(df):
    return df.groupby("date", as_index=False)["amount"].sum()

def weekly_summary(df):
    x = df.copy()
    x["week"] = x["date"].dt.to_period("W").astype(str)
    return x.groupby("week", as_index=False)["amount"].sum()

def estimate_monthly(df):
    if df.empty:
        return 0
    days = max((df["date"].max() - df["date"].min()).days + 1, 1)
    return float(df["amount"].sum() / days * 30)

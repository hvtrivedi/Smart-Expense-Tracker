import pandas as pd
import numpy as np

def forecast_monthly(df):
    """Simple linear trend estimate over daily spending.

    This is intentionally lightweight for a Tiny Project.
    """
    daily = df.groupby("date")["amount"].sum().reset_index()
    if len(daily) < 3:
        return float(daily["amount"].sum()) if len(daily) else 0.0

    daily["day_no"] = np.arange(len(daily))
    x = daily["day_no"].values
    y = daily["amount"].values
    slope, intercept = np.polyfit(x, y, 1)

    last_day = x[-1]
    future_days = np.arange(last_day + 1, last_day + 31)
    forecast = intercept + slope * future_days
    forecast = np.maximum(forecast, 0)
    return float(forecast.sum())

import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id", "date", "merchant", "amount",
    "category", "payment_method", "description"
]

def clean_transactions(df: pd.DataFrame):
    data = df.copy()
    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")

    before = len(data)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")

    data = data.dropna(subset=["transaction_id", "date", "amount", "merchant"])
    data = data[data["amount"] > 0]
    data["category"] = data["category"].fillna("Other").astype(str).str.strip()
    data["payment_method"] = data["payment_method"].fillna("Unknown").astype(str).str.strip()
    data["merchant"] = data["merchant"].astype(str).str.strip()
    data["description"] = data["description"].fillna("").astype(str).str.strip()

    duplicate_count = data.duplicated(subset=["transaction_id"]).sum()
    data = data.drop_duplicates(subset=["transaction_id"])

    data = data.sort_values("date").reset_index(drop=True)
    report = {
        "rows_before": before,
        "rows_after": len(data),
        "duplicates_removed": int(duplicate_count),
        "invalid_rows_removed": int(before - len(data) - duplicate_count)
    }
    return data, report

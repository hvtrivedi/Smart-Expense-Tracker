from analysis import category_summary, weekly_summary, estimate_monthly

def generate_insights(df):
    if df.empty:
        return ["No transaction data available."]

    insights = []
    cat = category_summary(df)
    top_cat = cat.iloc[0]
    total = df["amount"].sum()
    share = top_cat["amount"] / total * 100
    insights.append(
        f"{top_cat['category']} is your highest spending category "
        f"at ₹{top_cat['amount']:,.0f} ({share:.1f}% of total spending)."
    )

    weeks = weekly_summary(df)
    if len(weeks) >= 2:
        current = weeks.iloc[-1]["amount"]
        previous = weeks.iloc[-2]["amount"]
        if previous:
            change = (current - previous) / previous * 100
            direction = "increased" if change >= 0 else "decreased"
            insights.append(
                f"Spending {direction} by {abs(change):.1f}% in the latest week "
                f"compared with the previous week."
            )

    top_txn = df.loc[df["amount"].idxmax()]
    insights.append(
        f"Your highest single transaction was ₹{top_txn['amount']:,.0f} "
        f"at {top_txn['merchant']}."
    )

    insights.append(
        f"Estimated 30-day spending from the current daily average is "
        f"₹{estimate_monthly(df):,.0f}."
    )
    return insights

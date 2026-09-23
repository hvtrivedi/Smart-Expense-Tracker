import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from preprocessing import clean_transactions
from analysis import summary, category_summary, payment_summary, daily_summary, estimate_monthly
from insights import generate_insights
from prediction import forecast_monthly

st.set_page_config(page_title="Smart Expense Analyzer", page_icon="💰", layout="wide")

st.title("💰 Smart Expense Analyzer")
st.caption("Python-based personal expense tracking and data analysis")

@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

uploaded = st.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded is None:
    st.info("Upload transactions.csv from the project's data folder to start.")
    st.stop()

try:
    raw = load_data(uploaded)
    df, report = clean_transactions(raw)
except Exception as e:
    st.error(f"Could not process the file: {e}")
    st.stop()

st.sidebar.header("Filters")
categories = ["All"] + sorted(df["category"].unique().tolist())
selected = st.sidebar.selectbox("Category", categories)
payments = ["All"] + sorted(df["payment_method"].unique().tolist())
selected_payment = st.sidebar.selectbox("Payment method", payments)

filtered = df.copy()
if selected != "All":
    filtered = filtered[filtered["category"] == selected]
if selected_payment != "All":
    filtered = filtered[filtered["payment_method"] == selected_payment]

if filtered.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

s = summary(filtered)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Spending", f"₹{s['total_spending']:,.0f}")
c2.metric("Transactions", f"{s['transactions']:,}")
c3.metric("Average / Transaction", f"₹{s['average_transaction']:,.0f}")
c4.metric("Estimated 30-Day Spend", f"₹{estimate_monthly(filtered):,.0f}")

st.subheader("Spending by Category")
cat = category_summary(filtered)
fig, ax = plt.subplots()
ax.bar(cat["category"], cat["amount"])
ax.set_ylabel("Amount (₹)")
ax.set_xlabel("Category")
ax.tick_params(axis="x", rotation=35)
st.pyplot(fig, clear_figure=True)

st.subheader("Daily Spending Trend")
daily = daily_summary(filtered)
fig, ax = plt.subplots()
ax.plot(daily["date"], daily["amount"], marker="o")
ax.set_ylabel("Amount (₹)")
ax.set_xlabel("Date")
fig.autofmt_xdate()
st.pyplot(fig, clear_figure=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Payment Method")
    pay = payment_summary(filtered)
    fig, ax = plt.subplots()
    ax.pie(pay["amount"], labels=pay["payment_method"], autopct="%1.1f%%")
    st.pyplot(fig, clear_figure=True)

with col2:
    st.subheader("Budget Monitor")
    budget = st.number_input("Monthly budget (₹)", min_value=0.0, value=20000.0, step=1000.0)
    spent = s["total_spending"]
    if budget > 0:
        usage = min(spent / budget, 1.0)
        st.progress(usage)
        st.write(f"Spent: **₹{spent:,.0f}**")
        st.write(f"Remaining: **₹{max(budget - spent, 0):,.0f}**")
        if spent > budget:
            st.error("Monthly budget exceeded.")
        elif spent >= budget * 0.8:
            st.warning("You have used more than 80% of the budget.")
        else:
            st.success("Spending is currently within the budget.")

st.subheader("Smart Insights")
for insight in generate_insights(filtered):
    st.write("• " + insight)

st.subheader("30-Day Trend Forecast")
forecast = forecast_monthly(filtered)
st.write(f"Estimated spending for the next 30 days based on the recent daily trend: **₹{forecast:,.0f}**")
st.caption("This is a simple analytical forecast for educational purposes, not financial advice.")

with st.expander("Data Quality Report"):
    st.write(report)
    st.dataframe(filtered, use_container_width=True)

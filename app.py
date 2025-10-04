import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Load data
df = pd.read_csv("../DataSet/Nifty.csv/Stocks_2025.csv")
df = df.drop("Unnamed: 0", axis=1)

# Data preprocessing
df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()
df.Date = pd.to_datetime(df.Date)
df.Stock = df.Stock.replace(" ", "", regex=True)

# Streamlit UI
st.title("📈 Nifty Stock Analysis Dashboard")

# Select Category
categories = df["Category"].unique()
category = st.selectbox("Select Category:", categories)

# Filter by category
d = df[df["Category"] == category]

# Select Stock
stocks = d["Stock"].unique()
stock = st.selectbox("Select Stock:", stocks)

# Filter by stock
r = d[d["Stock"] == stock]

# Plot
fig, ax = plt.subplots(figsize=(12,6))
sb.lineplot(x=r["Date"], y=r["Close"], color='g', marker='*', label="Close Price", ax=ax)
sb.lineplot(x=r["Date"], y=r["SMA_50"], color='b', label="SMA 50", ax=ax)
sb.lineplot(x=r["Date"], y=r["SMA_200"], color='r', label="SMA 200", ax=ax)

plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Price")
plt.title(f"{stock} Stock Price with SMA (50 & 200)")
plt.legend()

# Show in Streamlit
st.pyplot(fig)

# Optional: Show data
st.subheader("📊 Data Preview")
st.dataframe(r.tail(20))

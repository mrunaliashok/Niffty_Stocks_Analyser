import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sb

# --- Load CSV safely ---
try:
    df = pd.read_csv("Stocks_2025.csv")
except FileNotFoundError:
    st.error("CSV file not found. Check the file path.")
    st.stop()

# --- Drop unnecessary columns ---
if "Unnamed: 0" in df.columns:
    df = df.drop("Unnamed: 0", axis=1)

# --- Clean Stock column ---
if "Stock" in df.columns:
    df["Stock"] = df["Stock"].str.replace(" ", "", regex=True)

# --- Parse Date safely ---
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # invalid dates become NaT
    if df["Date"].isna().any():
        st.warning("Some dates could not be parsed and are set as NaT.")
else:
    st.error("Date column not found in CSV.")
    st.stop()

# --- Compute rolling averages ---
if "Close" in df.columns:
    df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
    df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()
else:
    st.error("Close column not found in CSV.")
    st.stop()

# --- Streamlit UI ---
st.title("Nifty Stocks Analysis")

# Select stock
stock_list = df["Stock"].unique()
selected_stock = st.selectbox("Select Stock", stock_list)

# Filter data
filtered_df = df[df["Stock"] == selected_stock]

# Display table
st.dataframe(filtered_df)

# Plot Close price and SMA
plt.figure(figsize=(12,6))
plt.plot(filtered_df["Date"], filtered_df["Close"], label="Close Price")
plt.plot(filtered_df["Date"], filtered_df["SMA_50"], label="SMA 50")
plt.plot(filtered_df["Date"], filtered_df["SMA_200"], label="SMA 200")
plt.xlabel("Date")
plt.ylabel("Price")
plt.title(f"{selected_stock} Price Analysis")
plt.legend()
plt.xticks(rotation=45)
st.pyplot(plt)




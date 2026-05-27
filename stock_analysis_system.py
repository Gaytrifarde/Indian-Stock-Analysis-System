import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# INDIAN STOCK ANALYSIS SYSTEM
# SMA + EMA + BUY/SELL SIGNAL
# ==========================================

print("===================================")
print(" INDIAN STOCK ANALYSIS SYSTEM ")
print("===================================")

# ==========================================
# USER INPUT
# ==========================================

stock = input("\nEnter Indian Stock Symbol: ").upper()

# Add .NS automatically
if ".NS" not in stock:
    stock = stock + ".NS"

print("\nDownloading Live Stock Data...\n")

# ==========================================
# DOWNLOAD LIVE DATA
# ==========================================

data = yf.download(
    stock,
    period="6mo",
    interval="1d",
    auto_adjust=True
)

# ==========================================
# CHECK VALID STOCK
# ==========================================

if data.empty:
    print("Invalid Stock Symbol")
    exit()

# ==========================================
# DISPLAY DOWNLOADED DATA
# ==========================================

print("===================================")
print(" DOWNLOADED LIVE STOCK DATA ")
print("===================================")

print(data[["Open", "High", "Low", "Close", "Volume"]].tail(10))

# ==========================================
# SAVE CSV FILE
# ==========================================

data.to_csv(f"{stock}_data.csv")

print(f"\nCSV File Saved As: {stock}_data.csv")

# ==========================================
# CALCULATE SMA & EMA
# ==========================================

close_price = data["Close"].squeeze()

# 50 SMA
data["SMA_50"] = close_price.rolling(window=50).mean()

# 20 EMA
data["EMA_20"] = close_price.ewm(span=20, adjust=False).mean()

# ==========================================
# LATEST VALUES
# ==========================================

latest_close = float(close_price.iloc[-1])

latest_ema = float(data["EMA_20"].iloc[-1])

latest_sma = float(data["SMA_50"].iloc[-1])

prev_ema = float(data["EMA_20"].iloc[-2])

prev_sma = float(data["SMA_50"].iloc[-2])

# ==========================================
# SIGNAL GENERATION
# ==========================================

if prev_ema < prev_sma and latest_ema > latest_sma:
    signal = "STRONG BUY"

elif prev_ema > prev_sma and latest_ema < latest_sma:
    signal = "STRONG SELL"

elif latest_ema > latest_sma:
    signal = "BUY TREND"

elif latest_ema < latest_sma:
    signal = "SELL TREND"

else:
    signal = "HOLD"

# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n===================================")
print(" STOCK ANALYSIS RESULT ")
print("===================================")

print(f"\nStock : {stock}")

print(f"\nCurrent Price : ₹{round(latest_close, 2)}")

print(f"\n20 EMA : {round(latest_ema, 2)}")

print(f"50 SMA : {round(latest_sma, 2)}")

print(f"\nTRADING SIGNAL : {signal}")

# ==========================================
# GRAPH
# ==========================================

plt.figure(figsize=(14,7))

plt.plot(data.index, close_price, label="Closing Price")

plt.plot(data.index, data["SMA_50"], label="50 SMA")

plt.plot(data.index, data["EMA_20"], label="20 EMA")

plt.title(f"{stock} Stock Analysis")

plt.xlabel("Date")

plt.ylabel("Price")

plt.legend()

plt.grid(True)

plt.xlim(data.index.min(), data.index.max())

plt.show()

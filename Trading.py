import yfinance as yf
import numpy as np

companies = [
    "^GSPC","LTC","AAPL","MSFT", "GOOGL", "AMZN", "NVDA", "META","TSLA","DX-Y.NYB","^XDN",
    "^DJI","GC=F","AMD","RTX", "IBM","ETH-USD","SOL", "BTC-USD","WBD","INTC","^XDA"
]


def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = delta.where(delta < 0, 0).abs()
    avg_gain = gain.ewm(span=window, min_periods=window).mean()
    avg_loss = loss.ewm(span=window, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def trade_signal(rsi):
    if rsi < 30:
        return 'Good Trade'
    elif 30 < rsi < 45:
        return 'Minor Good Trade'
    elif 45 < rsi < 55 :
        return "Completely Even Trade"
    elif 55 < rsi < 70:
        return "Minor Bad Trade"
    elif rsi > 70:
        return 'Bad Trade'
    return 'No Signal'

results = []
for company in companies:
    try:
        data = yf.download(company, period="max", interval='1h', progress=False)
        if data.empty or len(data) < 15:
            print(f"Skipping {company}: insufficient data")
            continue
        data['RSI'] = calculate_rsi(data)
        latest_rsi = data['RSI'].dropna().iloc[-1]
        signal = trade_signal(latest_rsi)
        results.append((company, latest_rsi, signal))
    except Exception as e:
        print(f"Error processing {company}: {e}")

results.sort(key=lambda x: x[1])

print("\nRanked by RSI (Best to Worst):")
for comp, rsi, signal in results:
    print(f"{comp}: {rsi:.2f}, {signal}")

if results:
    best = results[0]
    worst = results[-1]
    print(f"\n Best RSI: {best[0]} with RSI {best[1]:.2f} ({best[2]})")
    print(f" Worst RSI: {worst[0]} with RSI {worst[1]:.2f} ({worst[2]})")
else:
    print("No valid RSI data available.")
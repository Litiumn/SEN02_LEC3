import yfinance as yf
from datetime import datetime

# 1. Define stocks to track
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META']

# 2. HTML Header
html = """
<html>
<head>
    <meta http-equiv="refresh" content="60">
    <style>
        body { font-family: Arial; text-align: center; padding: 20px; }
        table { margin: 0 auto; border-collapse: collapse; width: 60%; }
        th, td { padding: 12px; border-bottom: 1px solid #ddd; }
        .green { color: green; font-weight: bold; }
        .red { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Tech Trend Tracker</h1>
    <p>Last Updated: """ + datetime.now().strftime("%H:%M:%S") + """</p>
    <table>
        <tr><th>Stock</th><th>Price ($)</th><th>Trend</th></tr>
"""

# 3. Fetch Data
print("Fetching data...") # Console log for you
for symbol in tickers:
    try:
        stock = yf.Ticker(symbol)
        # Get 2 days of data to compare Close vs Open
        data = stock.history(period="2d")

        if not data.empty:
            current = data['Close'].iloc[-1]
            open_price = data['Open'].iloc[-1]
            diff = current - open_price

            # Determine color and arrow
            color = "green" if diff >= 0 else "red"
            arrow = "▲" if diff >= 0 else "▼"

            html += f"<tr><td>{symbol}</td><td>{current:.2f}</td><td class='{color}'>{arrow} {diff:.2f}</td></tr>"
            print(f"Processed {symbol}")
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# 4. Close HTML
html += "</table></body></html>"

# 5. Save to file
with open("/var/www/html/index.html", "w") as f:
    f.write(html)
print("Done! index.html created.")

# 6 or 7 or 8

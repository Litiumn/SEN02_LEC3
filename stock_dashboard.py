import yfinance as yf
from datetime import datetime
import json

# 1. Define stocks to track
tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META',
    'NFLX', 'AMD', 'INTC', 'ORCL', 'CRM', 'ADBE', 'CSCO',
    'PYPL', 'UBER', 'SNAP', 'TWLO', 'SQ', 'SHOP', 'SPOT',
    'ABNB', 'COIN', 'RBLX', 'ZM', 'DOCU', 'SNOW', 'PLTR'
]

# 2. Fetch Data
print("Fetching data...")
stock_data = []

for symbol in tickers:
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="2d")

        if not data.empty:
            current = data['Close'].iloc[-1]
            open_price = data['Open'].iloc[-1]
            diff = current - open_price
            percent_change = (diff / open_price) * 100

            stock_data.append({
                'symbol': symbol,
                'price': round(current, 2),
                'change': round(diff, 2),
                'percent': round(percent_change, 2),
                'direction': 'up' if diff >= 0 else 'down'
            })
            print(f"Processed {symbol}")
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# 3. Generate HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="60">
    <title>Tech Trend Tracker</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }}
        .gradient-text {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .update-time {{ text-align: center; color: #666; margin-bottom: 30px; font-size: 0.9em; }}
        .controls {{ display: flex; justify-content: space-between; margin-bottom: 20px; gap: 15px; }}
        .search-box {{ padding: 10px 15px; border: 2px solid #ddd; border-radius: 8px; width: 250px; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; table-layout: fixed; }}
        thead {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
        th {{ padding: 15px; text-align: left; cursor: pointer; }}
        
        /* Align numbers to the right */
        th:nth-child(2), th:nth-child(3), th:nth-child(4),
        td:nth-child(2), td:nth-child(3), td:nth-child(4) {{ text-align: right; }}

        td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .symbol {{ font-weight: bold; color: #333; }}
        
        .trend {{
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            justify-content: flex-end;
            gap: 5px;
            width: 100%; /* Ensures alignment works within the cell */
            white-space: nowrap;
        }}
        .up {{ color: #10b981; }}
        .down {{ color: #ef4444; }}
        
        .pagination button {{ padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer; }}
        .pagination button:disabled {{ background: #ccc; }}
    </style>
</head>
<body>
    <div class="container">
        <h1><span>📈</span><span class="gradient-text">Tech Trend Tracker</span></h1>
        <p class="update-time">Last Updated: {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}</p>
        
        <div class="controls">
            <input type="text" class="search-box" id="searchBox" placeholder="Search stocks...">
            <div class="pagination">
                <button id="prevBtn">←</button>
                <span id="pageInfo">Page 1</span>
                <button id="nextBtn">→</button>
            </div>
        </div>
        
        <table id="stockTable">
            <thead>
                <tr>
                    <th onclick="sortTable('symbol')">Stock Symbol</th>
                    <th onclick="sortTable('price')">Price ($)</th>
                    <th onclick="sortTable('change')">Change ($)</th>
                    <th onclick="sortTable('percent')">Change (%)</th>
                </tr>
            </thead>
            <tbody id="tableBody"></tbody>
        </table>
    </div>

    <script>
        const stockData = {json.dumps(stock_data)};
        let currentPage = 1;
        const itemsPerPage = 10;
        let filteredData = [...stockData];

        function renderTable() {{
            const tbody = document.getElementById('tableBody');
            const start = (currentPage - 1) * itemsPerPage;
            const pageData = filteredData.slice(start, start + itemsPerPage);
            
            tbody.innerHTML = pageData.map(stock => `
                <tr>
                    <td class="symbol">${{stock.symbol}}</td>
                    <td class="price">$${{stock.price.toFixed(2)}}</td>
                    <td class="trend ${{stock.direction}}">
                        <span>${{stock.direction === 'up' ? '▲' : '▼'}}</span>
                        ${{Math.abs(stock.change).toFixed(2)}}
                    </td>
                    <td class="trend ${{stock.direction}}">
                        <span>${{stock.direction === 'up' ? '▲' : '▼'}}</span>
                        ${{Math.abs(stock.percent).toFixed(2)}}%
                    </td>
                </tr>
            `).join('');
            
            document.getElementById('pageInfo').textContent = `Page ${{currentPage}}`;
            document.getElementById('prevBtn').disabled = currentPage === 1;
            document.getElementById('nextBtn').disabled = start + itemsPerPage >= filteredData.length;
        }}

        // Search logic
        document.getElementById('searchBox').addEventListener('input', (e) => {{
            const term = e.target.value.toLowerCase();
            filteredData = stockData.filter(s => s.symbol.toLowerCase().includes(term));
            currentPage = 1;
            renderTable();
        }});

        // Pagination buttons
        document.getElementById('prevBtn').onclick = () => {{ currentPage--; renderTable(); }};
        document.getElementById('nextBtn').onclick = () => {{ currentPage++; renderTable(); }};

        renderTable();
    </script>
</body>
</html>"""

with open("index.html", "w", encoding='utf-8') as f:
    f.write(html)
print("Done! Everything is now aligned.")

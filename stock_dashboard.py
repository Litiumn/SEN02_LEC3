import yfinance as yf
from datetime import datetime
import json

# 1. Define stocks to track - Expanded list
tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META',
    'NFLX', 'AMD', 'INTC', 'ORCL', 'CRM', 'ADBE', 'CSCO',
    'PYPL', 'UBER', 'SNAP', 'TWLO', 'SQ', 'SHOP', 'SPOT',
    'ABNB', 'COIN', 'RBLX', 'ZM', 'DOCU', 'SNOW', 'PLTR'
]

# 2. Fetch Data and store in a list
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

# 3. Generate HTML with embedded CSS and JavaScript
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="60">
    <title>Tech Trend Tracker</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
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
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        h1 span {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .update-time {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
        }}
        
        .controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .search-box {{
            padding: 10px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            width: 250px;
            transition: border-color 0.3s;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .pagination {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .pagination button {{
            padding: 8px 16px;
            border: none;
            background: #667eea;
            color: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.3s;
        }}
        
        .pagination button:hover:not(:disabled) {{
            background: #764ba2;
        }}
        
        .pagination button:disabled {{
            background: #ccc;
            cursor: not-allowed;
        }}
        
        .page-info {{
            color: #666;
            font-size: 0.9em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            position: relative;
        }}
        
        th:hover {{
            background: rgba(255,255,255,0.1);
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
        }}
        
        tbody tr {{
            transition: background 0.2s;
        }}
        
        tbody tr:hover {{
            background: #f5f5f5;
        }}
        
        .symbol {{
            font-weight: bold;
            color: #333;
            font-size: 1.1em;
        }}
        
        .price {{
            font-size: 1.1em;
            color: #333;
        }}
        
        .trend {{
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .trend.up {{
            color: #10b981;
        }}
        
        .trend.down {{
            color: #ef4444;
        }}
        
        .arrow {{
            font-size: 1.2em;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.1em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .controls {{
                flex-direction: column;
            }}
            
            .search-box {{
                width: 100%;
            }}
            
            table {{
                font-size: 0.9em;
            }}
            
            th, td {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 <span>Tech Trend Tracker</span></h1>
        <p class="update-time">Last Updated: {datetime.now().strftime("%B %d, %Y at %H:%M:%S UTC")}</p>
        
        <div class="controls">
            <input type="text" class="search-box" id="searchBox" placeholder="Search stocks...">
            <div class="pagination">
                <button id="prevBtn">← Previous</button>
                <span class="page-info" id="pageInfo">Page 1</span>
                <button id="nextBtn">Next →</button>
            </div>
        </div>
        
        <table id="stockTable">
            <thead>
                <tr>
                    <th onclick="sortTable('symbol')">Stock Symbol</th>
                    <th onclick="sortTable('price')">Price ($)</th>
                    <th onclick="sortTable('percent')">Change (%)</th>
                    <th onclick="sortTable('change')">Change ($)</th>
                </tr>
            </thead>
            <tbody id="tableBody">
            </tbody>
        </table>
        <div id="noResults" class="no-results" style="display: none;">No stocks found</div>
    </div>

    <script>
        const stockData = {json.dumps(stock_data)};
        let currentPage = 1;
        const itemsPerPage = 10;
        let filteredData = [...stockData];
        let sortColumn = 'symbol';
        let sortDirection = 'asc';

        function renderTable() {{
            const tbody = document.getElementById('tableBody');
            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const pageData = filteredData.slice(start, end);
            
            if (pageData.length === 0) {{
                tbody.innerHTML = '';
                document.getElementById('noResults').style.display = 'block';
                document.getElementById('stockTable').style.display = 'none';
                return;
            }}
            
            document.getElementById('noResults').style.display = 'none';
            document.getElementById('stockTable').style.display = 'table';
            
            tbody.innerHTML = pageData.map(stock => `
                <tr>
                    <td class="symbol">${{stock.symbol}}</td>
                    <td class="price">$${{stock.price.toFixed(2)}}</td>
                    <td class="trend ${{stock.direction}}">
                        <span class="arrow">${{stock.direction === 'up' ? '▲' : '▼'}}</span>
                        ${{Math.abs(stock.percent).toFixed(2)}}%
                    </td>
                    <td class="trend ${{stock.direction}}">
                        <span class="arrow">${{stock.direction === 'up' ? '▲' : '▼'}}</span>
                        ${{Math.abs(stock.change).toFixed(2)}}
                    </td>
                </tr>
            `).join('');
            
            updatePagination();
        }}

        function updatePagination() {{
            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            document.getElementById('pageInfo').textContent = `Page ${{currentPage}} of ${{totalPages}}`;
            document.getElementById('prevBtn').disabled = currentPage === 1;
            document.getElementById('nextBtn').disabled = currentPage >= totalPages;
        }}

        function sortTable(column) {{
            if (sortColumn === column) {{
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            }} else {{
                sortColumn = column;
                sortDirection = 'asc';
            }}
            
            filteredData.sort((a, b) => {{
                let aVal = a[column];
                let bVal = b[column];
                
                if (typeof aVal === 'string') {{
                    return sortDirection === 'asc' 
                        ? aVal.localeCompare(bVal)
                        : bVal.localeCompare(aVal);
                }}
                
                return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
            }});
            
            currentPage = 1;
            renderTable();
        }}

        document.getElementById('searchBox').addEventListener('input', (e) => {{
            const searchTerm = e.target.value.toLowerCase();
            filteredData = stockData.filter(stock => 
                stock.symbol.toLowerCase().includes(searchTerm)
            );
            currentPage = 1;
            renderTable();
        }});

        document.getElementById('prevBtn').addEventListener('click', () => {{
            if (currentPage > 1) {{
                currentPage--;
                renderTable();
            }}
        }});

        document.getElementById('nextBtn').addEventListener('click', () => {{
            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            if (currentPage < totalPages) {{
                currentPage++;
                renderTable();
            }}
        }});

        // Initial render
        renderTable();
    </script>
</body>
</html>"""

# 4. Save to file
with open("/var/www/html/index.html", "w", encoding='utf-8') as f:
    f.write(html)
print("Done! index.html created with enhanced features.")

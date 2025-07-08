from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import get_search_results

app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['POST'])
async def search_products():
    """API endpoint for product search"""
    try:
        data = request.get_json()
        country = data.get('country', '').upper()
        query = data.get('query', '')
        data=get_search_results(user_query={"location": country, "query": query})
        return jsonify({"success": True, "results": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Simple frontend"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Price Comparison Tool</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
            button { background-color: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .results { margin-top: 30px; }
            .product { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
            .price { font-size: 18px; font-weight: bold; color: #007bff; }
            .loading { text-align: center; padding: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Price Comparison Tool</h1>
            <form id="searchForm">
                <div class="form-group">
                    <label for="country">Country:</label>
                    <select id="country" name="country" required>
                        <option value="">Select Country</option>
                        <option value="us">United States</option>
                        <option value="in">India</option>
                        <option value="uk">United Kingdom</option>
                        <option value="de">Germany</option>
                        <option value="ca">Canada</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="query">Product Query:</label>
                    <input type="text" id="query" name="query" placeholder="e.g., iPhone 16 Pro, 128GB" required>
                </div>
                <button type="submit">Search Products</button>
            </form>
            
            <div id="results" class="results"></div>
        </div>
        
        <script>
            document.getElementById('searchForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const country = document.getElementById('country').value;
                const query = document.getElementById('query').value;
                const resultsDiv = document.getElementById('results');
                
                resultsDiv.innerHTML = '<div class="loading">Searching for products...</div>';
                
                try {
                    const response = await fetch('/api/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ country, query })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success ) {
                        if (data.results.length === 0) {
                            resultsDiv.innerHTML = '<p>No products found for your query.</p>';
                        } else {
                            let html = `<h2>Found ${data.results.length} products:</h2>`;
                            data.results.forEach(product => {
                                html += `
                                    <div class="product">
                                        <h3><a href="${product.Link}" target="_blank">${product.ProductName}</a></h3>
                                        <div class="price">${product.Price}</div>
                                        <p><strong>Website:</strong> ${product.Link}</p>
                                        <p><strong>Seller:</strong> ${product.Seller}</p>
                                    </div>
                                `;
                            });
                            resultsDiv.innerHTML = html;
                        }
                    } else {
                        resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                    }
                } catch (error) {
                    resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
                }
            });
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
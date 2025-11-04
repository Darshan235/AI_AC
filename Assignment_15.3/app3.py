from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for search API
items = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999},
    {"id": 2, "name": "Phone", "category": "Electronics", "price": 699},
    {"id": 3, "name": "Book", "category": "Literature", "price": 15},
    {"id": 4, "name": "Headphones", "category": "Electronics", "price": 199},
]

@app.route('/search', methods=['GET'])
def search():
    """Search items based on query parameters."""
    name = request.args.get('name', '').lower()
    category = request.args.get('category', '').lower()
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', float('inf')))

    results = items

    if name:
        results = [item for item in results if name in item['name'].lower()]
    
    if category:
        results = [item for item in results if category in item['category'].lower()]
    
    results = [item for item in results if min_price <= item['price'] <= max_price]

    return jsonify({
        "count": len(results),
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True)

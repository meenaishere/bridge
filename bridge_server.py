from flask import Flask, request, jsonify
import cloudscraper

app = Flask(__name__)

# The "Browser" that bypasses Cloudflare
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

@app.route('/login', methods=['POST'])
def proxy_login():
    """
    Your bot calls THIS endpoint.
    This server calls Utkarsh.
    """
    data = request.json
    # Forward the request to Utkarsh
    try:
        r = scraper.post("https://online.utkarsh.com/web/Auth/login", json=data)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_courses', methods=['POST'])
def proxy_courses():
    token = request.headers.get('Authorization')
    scraper.headers.update({'Authorization': token})
    
    # Forward to V1 API
    r = scraper.post("https://online.utkarsh.com/api/v1/course/get-my-courses", json={})
    return jsonify(r.json()), r.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

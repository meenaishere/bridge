from flask import Flask, request, jsonify
import cloudscraper

app = Flask(__name__)

# 🟢 The Magic: CloudScraper acts like a Chrome Browser
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

UTKARSH_HOST = "https://online.utkarsh.com"

@app.route('/', methods=['GET'])
def health():
    return "Utkarsh Proxy is Alive! 🚀"

@app.route('/login', methods=['POST'])
def proxy_login():
    """Proxies the Login Request"""
    try:
        data = request.json
        # Forward to Real Utkarsh
        r = scraper.post(f"{UTKARSH_HOST}/web/Auth/login", json=data, timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_courses', methods=['POST'])
def proxy_courses():
    """Proxies the V1 Course List Request"""
    try:
        # Get token from the bot's request
        token = request.headers.get('Authorization')
        scraper.headers.update({'Authorization': token})
        
        # Forward to V1 API
        r = scraper.post(f"{UTKARSH_HOST}/api/v1/course/get-my-courses", json={}, timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/extract', methods=['POST'])
def proxy_extract():
    """Proxies the V1 Master Data Request (Extraction)"""
    try:
        data = request.json
        token = request.headers.get('Authorization')
        scraper.headers.update({'Authorization': token})
        
        r = scraper.post(f"{UTKARSH_HOST}/api/v1/course/get-master-data", json=data, timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()

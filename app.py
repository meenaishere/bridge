from flask import Flask, request, jsonify
import cloudscraper

app = Flask(__name__)

# CloudScraper to act like Chrome
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

UTKARSH_HOST = "https://online.utkarsh.com"

@app.route('/', methods=['GET'])
def health():
    return "Utkarsh Dual-Proxy is Alive! 🚀"

@app.route('/login', methods=['POST'])
def proxy_login():
    try:
        data = request.json
        # Login is always via Web Auth
        r = scraper.post(f"{UTKARSH_HOST}/web/Auth/login", json=data, timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_courses', methods=['POST'])
def proxy_courses():
    """
    🔥 UPGRADED: Checks BOTH App and Web endpoints
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "No Token Provided"}), 401

    scraper.headers.update({
        'Authorization': token,
        'token': token.replace("Bearer ", "")
    })
    
    all_courses = []
    
    # 🟢 ROOM 1: The App API (V1)
    try:
        print("Checking V1 API...")
        r1 = scraper.post(f"{UTKARSH_HOST}/api/v1/course/get-my-courses", json={}, timeout=20)
        if r1.status_code == 200:
            data = r1.json().get('data', [])
            if isinstance(data, list):
                all_courses.extend(data)
    except Exception as e:
        print(f"V1 Error: {e}")
    
    # 🟢 ROOM 2: The Web API (Library/Legacy)
    try:
        print("Checking Web API...")
        r2 = scraper.post(f"{UTKARSH_HOST}/web/User/my_course_list", json={}, timeout=20)
        if r2.status_code == 200:
            data = r2.json().get('data', [])
            if isinstance(data, list):
                all_courses.extend(data)
    except Exception as e:
        print(f"Web Error: {e}")

    # 🟢 Filter Duplicates (If a course appears in both)
    unique_courses = {c['id']: c for c in all_courses}.values()
    
    final_list = list(unique_courses)
    print(f"✅ Total Found: {len(final_list)}")
    
    return jsonify({"data": final_list}), 200

@app.route('/extract', methods=['POST'])
def proxy_extract():
    try:
        data = request.json
        token = request.headers.get('Authorization')
        scraper.headers.update({'Authorization': token})
        
        # Extraction uses V1 Master Data
        r = scraper.post(f"{UTKARSH_HOST}/api/v1/course/get-master-data", json=data, timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()

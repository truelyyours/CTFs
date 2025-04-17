from flask import Flask, request, jsonify
import urllib.parse
import requests

app = Flask(__name__)

@app.route('/secret', methods=['GET'])
def secret():
    # Allow access only from localhost
    if request.remote_addr != '127.0.0.1':
        return 'Access denied', 403
    return 'EPFL{fake_flag}', 200

@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url', '')
    if not url:
        return 'Missing url parameter', 400

    # Replace backslashes with slashes
    url = url.replace('\\', '/')
    parsed = urllib.parse.urlparse(url)

    # Check for valid protocol
    if parsed.scheme not in ['http', 'https']:
        return 'invalid protocol', 400

    # Check for custom port
    if parsed.port:
        return 'no custom port allowed', 400

    # Forward the request to the second proxy
    try:
        response = requests.post('http://localhost:1111/proxy', json={'url': url}, timeout=5)
        return response.text, response.status_code
    except requests.exceptions.RequestException:
        return 'Error contacting second proxy', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9222)

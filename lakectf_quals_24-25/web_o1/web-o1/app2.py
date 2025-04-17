from flask import Flask, request, jsonify
import urllib.parse
import socket
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['POST'])
def proxy():
    data = request.get_json()
    if not data or 'url' not in data:
        return 'Missing url parameter', 400

    url = data['url']
    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme
    hostname = parsed.hostname
    port = parsed.port

    # Determine the port if not explicitly specified
    if port is None:
        try:
            port = socket.getservbyname(scheme)
        except:
            return 'Invalid scheme', 400

    # Validate the target domain based on the port
    if (port == 443 and hostname != 'example.com') or (port == 80 and hostname != 'example.net'):
        return 'invalid target domain!', 400

    # Forward the request to the third proxy
    try:
        response = requests.post('http://localhost:3000/proxy', json={'url': url}, timeout=5)
        return response.text, response.status_code
    except requests.exceptions.RequestException:
        return 'Error contacting third proxy', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111)

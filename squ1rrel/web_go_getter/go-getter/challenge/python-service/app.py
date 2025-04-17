from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

GO_HAMSTER_IMAGES = [
    {
        "name": "boring gopher",
        "src": "https://camo.githubusercontent.com/a72f086b878c2e74b90d5dbd3360e7a4aa132a219a662f4d83b7c243298fea4d/68747470733a2f2f7261772e6769746875622e636f6d2f676f6c616e672d73616d706c65732f676f706865722d766563746f722f6d61737465722f676f706865722e706e67"
    },
    {
        "name": "gopher plush",
        "src": "https://go.dev/blog/gopher/plush.jpg"
    },
    {
        "name": "fairy gopher",
        "src": "https://miro.medium.com/v2/resize:fit:1003/1*lzAGEWMWtgn3NnRECl8gmw.png"
    },
    {
        "name": "scientist gopher",
        "src": "https://miro.medium.com/v2/resize:fit:1400/1*Xxckk9KBW73GWgxhtJN5nA.png"
    },
    {
        "name": "three gopher",
        "src": "https://go.dev/blog/gopher/header.jpg"
    },
    {
        "name": "hyperrealistic gopher",
        "src": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPNG7wGmWuHcSi7Wkzmht8TSdeXAHOl5edBw&s"
    },
    {
        "name": "flyer gopher",
        "src": "https://upload.wikimedia.org/wikipedia/commons/d/df/Go_gopher_app_engine_color.jpg"
    }
]

@app.route('/execute', methods=['POST'])
def execute():
    # Ensure request has JSON
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    
    # Check if action key exists
    if 'action' not in data:
        return jsonify({"error": "Missing 'action' key"}), 400

    # Process action
    if data['action'] == "getgopher":
        # choose random gopher
        gopher = random.choice(GO_HAMSTER_IMAGES)
        return jsonify(gopher)
    elif data['action'] == "getflag":
        return jsonify({"flag": os.getenv("FLAG")})
    else:
        return jsonify({"error": "Invalid action"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

t = 0.0

@app.route('/app/data', methods=['GET'])
def get_data():
    global t
    response_data = {
        # "message": "Hello, this is a JSON response!",
        # "status": "success",
        "x": 2 * math.sin(t) - 2,
        "y": 10,
        "z": 2 * math.cos(t) + 0
    }
    t += 0.01
    return jsonify(response_data), 200  # Sending HTTP status 200 (OK)
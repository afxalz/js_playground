from flask import Flask, jsonify
from flask_cors import CORS
from butter_tunnel_simulator import BtSimulator

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

bt_simulator = BtSimulator(100)

@app.route('/app/data', methods=['GET'])
def get_data():
    bt_simulator.step()
    # print(bt_simulator.get_positions())
    return jsonify(bt_simulator.get_positions()), 200  # Sending HTTP status 200 (OK)
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from collections import deque
import queue
import threading
import os

app = Flask(__name__, static_folder='ui/dist')
CORS(app)

class DataManager:
    def __init__(self, max_points=1000):
        self.max_points = max_points
        self.mandelbrot_data = None
        self.game_theory_history = {
            'rounds': deque(maxlen=max_points),
            'cooperate': deque(maxlen=max_points),
            'defect': deque(maxlen=max_points),
            'tit_for_tat': deque(maxlen=max_points)
        }
        self.gpu_stats = {
            'temperature': deque(maxlen=max_points),
            'utilization': deque(maxlen=max_points)
        }

    def process_data(self, data):
        if data['type'] == 'game_theory':
            self.game_theory_history['rounds'].append(data['round'])
            self.game_theory_history['cooperate'].append(data['populations'][0])
            self.game_theory_history['defect'].append(data['populations'][1])
            self.game_theory_history['tit_for_tat'].append(data['populations'][2])
        elif data['type'] == 'mandelbrot':
            self.mandelbrot_data = data['matrix']
        elif data['type'] == 'gpu_stats':
            self.gpu_stats['temperature'].append(data['temperature'])
            self.gpu_stats['utilization'].append(data['utilization'])

    def get_data(self):
        return {
            'game_theory': {
                'rounds': list(self.game_theory_history['rounds']),
                'cooperate': list(self.game_theory_history['cooperate']),
                'defect': list(self.game_theory_history['defect']),
                'tit_for_tat': list(self.game_theory_history['tit_for_tat'])
            },
            'mandelbrot': self.mandelbrot_data,
            'gpu_stats': {
                'temperature': list(self.gpu_stats['temperature']),
                'utilization': list(self.gpu_stats['utilization'])
            }
        }

data_manager = DataManager()

@app.route('/update-data', methods=['POST'])
def update_data():
    data = request.json
    data_manager.process_data(data)
    return jsonify({"status": "success"})

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(data_manager.get_data())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    try:
        if path and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        elif os.path.exists(app.static_folder + '/index.html'):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({"message": "Visualization UI not found. Data API endpoints are still available."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def start_visualization_server():
    app.run(port=8050, debug=False, host='0.0.0.0')  # Less strict settings

if __name__ == "__main__":
    start_visualization_server()
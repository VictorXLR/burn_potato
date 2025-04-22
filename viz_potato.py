from flask import Flask, jsonify, request
from flask_cors import CORS
from collections import deque
import queue
import threading

app = Flask(__name__)
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
        self.gpu_stats = {'temperature': [], 'utilization': []}
        self.data_queue = queue.Queue()

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

data_manager = DataManager()

@app.route('/update-data', methods=['POST'])
def update_data():
    data = request.json
    data_manager.process_data(data)
    return jsonify({"status": "success"})

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify({
        'game_theory': {
            'rounds': list(data_manager.game_theory_history['rounds']),
            'cooperate': list(data_manager.game_theory_history['cooperate']),
            'defect': list(data_manager.game_theory_history['defect']),
            'tit_for_tat': list(data_manager.game_theory_history['tit_for_tat'])
        },
        'mandelbrot': data_manager.mandelbrot_data,
        'gpu_stats': data_manager.gpu_stats
    })

def start_visualization_server():
    app.run(port=8050)

if __name__ == "__main__":
    start_visualization_server()
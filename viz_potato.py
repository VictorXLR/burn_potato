import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import numpy as np
import json
import glob
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from collections import deque
import threading
import queue

class AnimationStream:
    def __init__(self, max_points=1000):
        self.app = Dash(__name__)
        self.data_queue = queue.Queue()
        self.max_points = max_points
        
        # Initialize data storage
        self.mandelbrot_data = None
        self.game_theory_history = {
            'rounds': deque(maxlen=max_points),
            'cooperate': deque(maxlen=max_points),
            'defect': deque(maxlen=max_points),
            'tit_for_tat': deque(maxlen=max_points)
        }
        
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1("GPU Potato Dashboard 🥔"),
            
            html.Div([
                dcc.Graph(id='game-theory-plot'),
                dcc.Graph(id='mandelbrot-plot'),
                dcc.Graph(id='gpu-stats-plot'),
                dcc.Interval(id='interval-component', interval=500)
            ])
        ])
    
    def setup_callbacks(self):
        @self.app.callback(
            [Output('game-theory-plot', 'figure'),
             Output('mandelbrot-plot', 'figure'),
             Output('gpu-stats-plot', 'figure')],
            Input('interval-component', 'n_intervals')
        )
        def update_graphs(n):
            # Process any new data in queue
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.process_data(data)
            
            # Game Theory Plot
            game_fig = go.Figure()
            for strategy in ['cooperate', 'defect', 'tit_for_tat']:
                game_fig.add_trace(go.Scatter(
                    x=list(self.game_theory_history['rounds']),
                    y=list(self.game_theory_history[strategy]),
                    name=strategy.title()
                ))
            game_fig.update_layout(title='Game Theory Evolution')
            
            # Mandelbrot Plot
            mandel_fig = go.Figure()
            if self.mandelbrot_data is not None:
                mandel_fig.add_trace(go.Heatmap(z=self.mandelbrot_data))
            mandel_fig.update_layout(title='Mandelbrot Set')
            
            # GPU Stats Plot
            stats_fig = go.Figure()
            # Add GPU temperature/utilization if available
            stats_fig.update_layout(title='GPU Metrics')
            
            return game_fig, mandel_fig, stats_fig
    
    def process_data(self, data):
        if data['type'] == 'game_theory':
            self.game_theory_history['rounds'].append(data['round'])
            self.game_theory_history['cooperate'].append(data['populations'][0])
            self.game_theory_history['defect'].append(data['populations'][1])
            self.game_theory_history['tit_for_tat'].append(data['populations'][2])
        elif data['type'] == 'mandelbrot':
            self.mandelbrot_data = data['matrix']
    
    def run(self, port=8050):
        self.app.run_server(debug=True, port=port)

def start_visualization_server():
    anim = AnimationStream()
    anim.run()

if __name__ == "__main__":
    start_visualization_server()
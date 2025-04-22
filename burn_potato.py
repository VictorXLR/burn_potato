import torch
import time
import sys
import numpy as np
import json
from datetime import datetime
import requests
import threading

VIZ_SERVER = "http://localhost:8050"

def stream_data(data):
    try:
        requests.post(f"{VIZ_SERVER}/update-data", json=data)
    except:
        pass  # Silently fail if visualization server is not running

def simulate_game_theory():
    print("🔍 Simulating game theory research: Live streaming Prisoner's Dilemma")
    strategies = ['Cooperate', 'Defect', 'TitForTat']
    population = np.array([1/3, 1/3, 1/3])
    payoff_matrix = np.array([
        [3, 0, 3],
        [5, 1, 5],
        [3, 0, 3]
    ])
    
    mutation_rate = 1e-4
    round_num = 0
    
    try:
        while True:
            round_num += 1
            expected_payoffs = payoff_matrix.dot(population)
            total = np.dot(population, expected_payoffs)
            
            new_population = population * expected_payoffs / total
            new_population = new_population + mutation_rate
            population = new_population / new_population.sum()
            
            # Stream data instead of printing
            stream_data({
                'type': 'game_theory',
                'round': round_num,
                'populations': population.tolist()
            })
            
            time.sleep(0.1)  # Faster updates for smoother animation
    except KeyboardInterrupt:
        print("\nSimulation ended")

def burn_potato():
    if not torch.cuda.is_available():
        print("No CUDA-capable GPU found. Your potato is not hot enough.")
        return

    device = torch.device("cuda")
    print(f"🔥 Burning potato on: {torch.cuda.get_device_name(device)}")

    size = 8192  # Larger size = more heat
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    try:
        while True:
            torch.matmul(a, b)
            torch.cuda.synchronize()
            print("🥔 Warming up... press Ctrl+C to stop.")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🧊 Potato cooling down. Stay warm!")


def expensive_game_theory():
    if not torch.cuda.is_available():
        print("No CUDA-capable GPU found. Expensive simulation cannot run.")
        return

    device = torch.device("cuda")
    print(f"🔥 Running expensive game theory simulation on: {torch.cuda.get_device_name(device)}")
    
    num_strategies = 1000  # Increased number of strategies for a heftier simulation
    # Initialize with a uniform distribution over strategies (GPU tensor)
    population = torch.full((num_strategies,), 1.0 / num_strategies, device=device)
    # Create a random payoff matrix with values between 0 and 10
    payoff_matrix = torch.randint(0, 11, (num_strategies, num_strategies), dtype=torch.float, device=device)
    
    mutation_rate = 1e-4  # small mutation factor
    
    round_num = 0
    try:
        while True:
            round_num += 1
            # Calculate expected payoffs for each strategy using matrix multiplication
            expected_payoffs = torch.matmul(payoff_matrix, population)
            # Compute total payoff using dot product
            total = torch.dot(population, expected_payoffs)
            # Update using replicator dynamics: new_population = population * (expected_payoff/total)
            new_population = population * expected_payoffs / total
            new_population = new_population + mutation_rate
            population = new_population / new_population.sum()
            
            # Report statistics every 10 rounds
            if round_num % 10 == 0:
                min_pop = population.min().item()
                max_pop = population.max().item()
                print(f"Round {round_num}: population stats -> min: {min_pop:.5f}, max: {max_pop:.5f}")
    except KeyboardInterrupt:
        print("\nExpensive simulation ended. Thank you for exploring advanced game theory research!")

def benchmark_matmul():
    if not torch.cuda.is_available():
        return
    device = torch.device("cuda")
    sizes = [1024, 2048, 4096, 8192]
    results = {}
    
    for size in sizes:
        a = torch.randn(size, size, device=device)
        b = torch.randn(size, size, device=device)
        
        start_time = time.time()
        for _ in range(10):
            torch.matmul(a, b)
            torch.cuda.synchronize()
        elapsed = (time.time() - start_time) / 10
        
        results[size] = elapsed
        print(f"Size {size}x{size}: {elapsed:.4f} seconds per multiplication")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"matmul_benchmark_{timestamp}.json", "w") as f:
        json.dump(results, f)

def generate_mandelbrot():
    if not torch.cuda.is_available():
        return
    device = torch.device("cuda")
    width, height = 1024, 1024
    max_iter = 256
    
    while True:  # Continuous generation
        x = torch.linspace(-2, 1, width, device=device)
        y = torch.linspace(-1.5, 1.5, height, device=device)
        X, Y = torch.meshgrid(x, y, indexing='ij')
        Z = X + 1j * Y
        C = Z.clone()
        
        mask = torch.zeros_like(Z, dtype=torch.int32, device=device)
        for i in range(max_iter):
            Z = Z * Z + C
            new_mask = torch.abs(Z) > 2.0
            mask[new_mask] = i
            Z[new_mask] = 0
        
        # Stream the result instead of saving
        stream_data({
            'type': 'mandelbrot',
            'matrix': mask.cpu().numpy().tolist()
        })
        time.sleep(0.1)

def analyze_gpu_noise():
    if not torch.cuda.is_available():
        return
    device = torch.device("cuda")
    samples = 10000000
    
    data = torch.randn(samples, device=device)
    stats = {
        "mean": data.mean().item(),
        "std": data.std().item(),
        "min": data.min().item(),
        "max": data.max().item(),
        "p25": torch.quantile(data, 0.25).item(),
        "p50": torch.quantile(data, 0.50).item(),
        "p75": torch.quantile(data, 0.75).item()
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"noise_stats_{timestamp}.json", "w") as f:
        json.dump(stats, f)
    print(f"Noise analysis saved to noise_stats_{timestamp}.json")

def simple_cnn_forward():
    if not torch.cuda.is_available():
        return
    device = torch.device("cuda")
    
    # Create a small CNN
    model = torch.nn.Sequential(
        torch.nn.Conv2d(3, 16, 3),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(2),
        torch.nn.Conv2d(16, 32, 3),
        torch.nn.ReLU(),
    ).to(device)
    
    # Generate random input
    batch_size = 100
    input_data = torch.randn(batch_size, 3, 32, 32, device=device)
    
    # Measure inference time
    times = []
    for _ in range(100):
        start = time.time()
        with torch.no_grad():
            output = model(input_data)
        torch.cuda.synchronize()
        times.append(time.time() - start)
    
    stats = {
        "mean_time": np.mean(times),
        "std_time": np.std(times),
        "min_time": np.min(times),
        "max_time": np.max(times)
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"cnn_inference_{timestamp}.json", "w") as f:
        json.dump(stats, f)
    print(f"CNN inference stats saved to cnn_inference_{timestamp}.json")

def start_gpu_monitor():
    while True:
        if torch.cuda.is_available():
            # Get GPU stats if available
            try:
                temp = torch.cuda.temperature()
                util = torch.cuda.utilization()
                stream_data({
                    'type': 'gpu_stats',
                    'temperature': temp,
                    'utilization': util
                })
            except:
                pass
        time.sleep(1)

functions_map = {
    '1': burn_potato,
    '2': simulate_game_theory,
    '3': expensive_game_theory,
    '4': benchmark_matmul,
    '5': generate_mandelbrot,
    '6': analyze_gpu_noise,
    '7': simple_cnn_forward
}

if __name__ == "__main__":
    # Start GPU monitoring in background
    monitor_thread = threading.Thread(target=start_gpu_monitor, daemon=True)
    monitor_thread.start()
    
    if len(sys.argv) != 2 or sys.argv[1] not in functions_map:
        print("Usage: python burn_potato.py [number]")
        print("Options:")
        for key, func in functions_map.items():
            print(f" {key}: {func.__name__}")
        sys.exit(1)
    
    selected_function = functions_map[sys.argv[1]]
    selected_function()
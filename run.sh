#!/bin/bash

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh [burn_option]"
    echo "Options:"
    echo " 1: Basic GPU Stress Test"
    echo " 2: Game Theory Evolution"
    echo " 3: Advanced Game Theory (GPU-heavy)"
    echo " 4: Matrix Multiplication Benchmark"
    echo " 5: Mandelbrot Set Generator"
    echo " 6: GPU Noise Analysis"
    echo " 7: CNN Forward Pass Test"
    exit 1
fi

# Start UI in background
cd ui && npm run build && cd ..
echo "Starting UI build..."

# Start visualization server in background
echo "Starting visualization server..."
python viz_potato.py &
VIZ_PID=$!

# Wait a bit for the server to start
sleep 2

# Run burn_potato with provided argument
echo "Starting GPU workload..."
python burn_potato.py $1

# Cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $VIZ_PID
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for user interrupt
wait
# 🥔 GPU Potato Project

A fun real-time GPU stress testing and visualization toolkit that turns your graphics card into a creative potato.

## Features

- **Real-time Visualizations**: Browser-based dashboard showing live animations
- **Mandelbrot Explorer**: GPU-accelerated Mandelbrot set visualization
- **Game Theory Simulator**: Watch strategies evolve in real-time
- **GPU Stress Testing**: Various methods to heat up your GPU
- **Performance Metrics**: Live GPU temperature and utilization monitoring

## Quick Start

1. Start the visualization server:

```bash
python viz_potato.py
```

2. Open your browser to `http://localhost:8050`

3. Run any simulation:

```bash
python burn_potato.py [option]
```

### Available Options

1. Basic GPU Stress Test
2. Game Theory Evolution
3. Advanced Game Theory (GPU-heavy)
4. Matrix Multiplication Benchmark
5. Mandelbrot Set Generator
6. GPU Noise Analysis
7. CNN Forward Pass Test

## Requirements

- Python 3.8+
- PyTorch with CUDA support
- Plotly & Dash
- NumPy
- A CUDA-capable GPU (the more powerful, the better)

## Fun Facts

- The Mandelbrot visualization uses complex number operations on the GPU
- The Game Theory simulator implements evolutionary dynamics
- All visualizations update in real-time without saving files
- Your GPU might actually get warm (hence the potato) 🔥

## Safety Note

This project is designed for fun and educational purposes. While it won't damage your GPU (modern GPUs have thermal protection), it will make it work hard. Monitor your temperatures!

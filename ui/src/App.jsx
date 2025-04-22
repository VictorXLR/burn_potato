import { useState, useEffect } from 'react'
import { Box, Container, Grid, Paper, Typography } from '@mui/material'
import Plot from 'react-plotly.js'

const API_URL = 'http://localhost:8050'

function App() {
  const [data, setData] = useState({
    gpu_stats: { temperature: [], utilization: [] },
    mandelbrot: null,
    game_theory: { rounds: [], cooperate: [], defect: [], tit_for_tat: [] }
  })

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}/get-data`)
        const newData = await response.json()
        setData(newData)
      } catch (error) {
        console.error('Failed to fetch data:', error)
      }
    }

    const interval = setInterval(fetchData, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>GPU Potato Monitor</Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', overflow: 'auto', flexDirection: 'column' }}>
            <Plot
              data={[{
                y: data.gpu_stats.temperature,
                name: 'Temperature (°C)',
                type: 'line'
              }, {
                y: data.gpu_stats.utilization,
                name: 'Utilization (%)',
                yaxis: 'y2',
                type: 'line'
              }]}
              layout={{
                title: 'GPU Stats',
                yaxis: { title: 'Temperature (°C)' },
                yaxis2: {
                  title: 'Utilization (%)',
                  overlaying: 'y',
                  side: 'right'
                }
              }}
              useResizeHandler
              style={{ width: '100%', height: '400px' }}
            />
          </Paper>
        </Grid>

        {data.mandelbrot && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2, display: 'flex', overflow: 'auto', flexDirection: 'column' }}>
              <Plot
                data={[{
                  z: data.mandelbrot,
                  type: 'heatmap',
                  colorscale: 'Viridis'
                }]}
                layout={{
                  title: 'Mandelbrot Set',
                  width: null,
                  height: null
                }}
                useResizeHandler
                style={{ width: '100%', height: '600px' }}
              />
            </Paper>
          </Grid>
        )}

        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', overflow: 'auto', flexDirection: 'column' }}>
            <Plot
              data={[{
                x: data.game_theory.rounds,
                y: data.game_theory.cooperate,
                name: 'Cooperate',
                type: 'scatter'
              }, {
                x: data.game_theory.rounds,
                y: data.game_theory.defect,
                name: 'Defect',
                type: 'scatter'
              }, {
                x: data.game_theory.rounds,
                y: data.game_theory.tit_for_tat,
                name: 'Tit for Tat',
                type: 'scatter'
              }]}
              layout={{
                title: 'Game Theory Evolution',
                xaxis: { title: 'Rounds' },
                yaxis: { title: 'Population' }
              }}
              useResizeHandler
              style={{ width: '100%', height: '400px' }}
            />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  )
}

export default App
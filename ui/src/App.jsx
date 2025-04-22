import { useState, useEffect } from 'react'
import { Box, Container, Typography, Grid } from '@mui/material'
import Plot from 'react-plotly.js'

const API_URL = 'http://localhost:8050'

function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`${API_URL}/get-data`)
      const newData = await response.json()
      setData(newData)
    }

    const interval = setInterval(fetchData, 1000)
    return () => clearInterval(interval)
  }, [])

  if (!data) return <Typography>Loading...</Typography>

  return (
    <Container>
      <Typography variant="h3" gutterBottom>Potato Monitor</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Plot
            data={[
              {
                x: data.game_theory.rounds,
                y: data.game_theory.cooperate,
                name: 'Cooperate',
                type: 'scatter'
              },
              {
                x: data.game_theory.rounds,
                y: data.game_theory.defect,
                name: 'Defect',
                type: 'scatter'
              },
              {
                x: data.game_theory.rounds,
                y: data.game_theory.tit_for_tat,
                name: 'Tit for Tat',
                type: 'scatter'
              }
            ]}
            layout={{ title: 'Game Theory Evolution' }}
            style={{ width: '100%', height: '400px' }}
          />
        </Grid>
        {data.mandelbrot_data && (
          <Grid item xs={12}>
            <Plot
              data={[{
                z: data.mandelbrot_data,
                type: 'heatmap'
              }]}
              layout={{ title: 'Mandelbrot Set' }}
              style={{ width: '100%', height: '600px' }}
            />
          </Grid>
        )}
        <Grid item xs={12}>
          <Plot
            data={[
              {
                y: data.gpu_stats.temperature,
                name: 'Temperature',
                type: 'line'
              },
              {
                y: data.gpu_stats.utilization,
                name: 'Utilization',
                type: 'line',
                yaxis: 'y2'
              }
            ]}
            layout={{
              title: 'GPU Stats',
              yaxis: { title: 'Temperature (°C)' },
              yaxis2: {
                title: 'Utilization (%)',
                overlaying: 'y',
                side: 'right'
              }
            }}
            style={{ width: '100%', height: '400px' }}
          />
        </Grid>
      </Grid>
    </Container>
  )
}

export default App
<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { 
  Chart as ChartJS, Title, Tooltip, Legend, BarElement, 
  CategoryScale, LinearScale 
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps(['histogramData', 'varValue'])

const chartData = computed(() => {
  if (!props.histogramData) return { labels: [], datasets: [] }

  const rawVar = parseFloat(props.varValue)
  const threshold = 1 + (rawVar / 100)

  return {
    labels: props.histogramData.bins.map(b => b.toFixed(2)),
    datasets: [
      {
        label: 'SIMULATIONS',
        backgroundColor: props.histogramData.bins.map(bin => {
          return bin <= (threshold + 0.001) ? '#ef4444' : 'rgba(63, 63, 70, 0.4)'
        }),
        borderColor: props.histogramData.bins.map(bin => 
          bin <= (threshold + 0.001) ? '#b91c1c' : '#3f3f46'
        ),
        borderWidth: 1,
        data: props.histogramData.counts,
        barPercentage: 0.9,
      }
    ]
  }
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { top: 40, left: 20, right: 20, bottom: 10 } },
  interaction: { mode: 'index', intersect: false },
  plugins: { 
    legend: { display: false },
    tooltip: {
      backgroundColor: '#18181b',
      titleFont: { family: "'JetBrains Mono', monospace" },
      bodyFont: { family: "'JetBrains Mono', monospace" },
      borderColor: '#3f3f46', 
      borderWidth: 1
    }
  },
  scales: {
    x: {
      title: { display: true, text: 'PORTFOLIO_GROWTH_FACTOR(1 YEAR)', color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 9 } },
      grid: { display: false },
      ticks: { color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 8 } }
    },
    y: {
      title: { display: true, text: 'FREQUENCY', color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 9 } },
      grid: { color: '#111' },
      ticks: { color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 8 } }
    }
  }
}
</script>

<template>
  <div style="width: 100%; height: 100%; position: relative;">
    <div class="chart-legend">
      <div class="legend-item" style="color: var(--accent-red-bright);">
        <div style="width: 12px; height: 12px; background-color: #dc2626; border: 1px solid var(--accent-red-bright); box-shadow: 0 0 10px rgba(239,68,68,0.3);"></div>
        <span>Tail_Risk_Zone (VaR_95)</span>
      </div>
    </div>
    
    <Bar :data="chartData" :options="options" />
  </div>
</template>
<script setup>
import { Line } from 'vue-chartjs'
import { ref, computed } from 'vue'
import { 
  Chart as ChartJS, Title, Tooltip, Legend, LineElement, 
  PointElement, CategoryScale, LinearScale, Filler 
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale, Filler)

const props = defineProps(['chartData']) 

const getPathColor = computed(() => {
  if (!props.chartData || !props.chartData.representative_path) return '#a1a1aa'
  const finalValue = props.chartData.representative_path.slice(-1)[0]
  return finalValue >= 1.0 ? '#00ff00' : '#ff3b3f' 
})

const chartConfig = computed(() => {
  if (!props.chartData || !props.chartData.representative_path) {
    return { labels: [], datasets: [] }
  }

  const { representative_path, path_95, path_05, all_paths } = props.chartData
  const labels = representative_path.map((_, i) => i)

  const spaghettiDatasets = all_paths.map((path, index) => ({
    label: `Path_${index}`,
    data: path,
    borderColor: 'rgba(63, 63, 70, 0.15)',
    borderWidth: 0.5,
    pointRadius: 0,
    order: 10,
    tension: 0.1
  }))

  return {
    labels,
    datasets: [
      ...spaghettiDatasets,
      {
        label: 'BOUND_95',
        data: path_95,
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderDash: [5, 5],
        borderWidth: 1,
        pointRadius: 0,
        fill: false,
        order: 1
      },
      {
        label: 'BOUND_05',
        data: path_05,
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderDash: [5, 5],
        borderWidth: 1,
        pointRadius: 0,
        fill: false,
        order: 1
      },
      {
        label: 'REPRESENTATIVE',
        data: representative_path,
        borderColor: getPathColor.value,
        borderWidth: 2.5,
        pointRadius: 0,
        order: 0,
        tension: 0.1
      }
    ]
  }
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { top: 40, left: 20, right: 20, bottom: 10 } },
  plugins: {
    legend: { display: false },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: '#18181b', 
      titleFont: { family: "'JetBrains Mono', monospace" },
      bodyFont: { family: "'JetBrains Mono', monospace" },
      borderColor: '#3f3f46', 
      borderWidth: 1
    }
  },
  scales: {
    x: {
      title: { display: true, text: 'TRADING_DAYS (T)', color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 9 } },
      grid: { color: '#111' },
      ticks: { color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 9 } }
    },
    y: {
      title: { display: true, text: 'PORTFOLIO_GROWTH_FACTOR', color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 9 } },
      grid: { color: '#111' },
      ticks: { color: '#52525b', font: { family: "'JetBrains Mono', monospace", size: 9 } }
    }
  }
}
</script>

<template>
  <div style="width: 100%; height: 100%; position: relative;">
    <div class="chart-legend">
      <span class="legend-item" style="color: var(--accent-green);">
        <div style="width: 12px; height: 2px; background-color: var(--accent-green); box-shadow: 0 0 8px rgba(52,211,153,0.4);"></div> 
        REP_PATH
      </span>
      <span class="legend-item" style="color: var(--text-dim);">
        <div style="width: 12px; height: 2px; border-top: 1px dashed var(--text-dim);"></div> 
        95%_CONFIDENCE_INTERVAL
      </span>
    </div>

    <Line :data="chartConfig" :options="options" />
  </div>
</template>
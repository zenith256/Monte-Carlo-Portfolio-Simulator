<script setup>
import { ref } from 'vue'
import axios from 'axios'
import SystemBoot from './components/SystemBoot.vue'
import PortfolioInput from './components/PortfolioInput.vue'
import SimulationResults from './components/SimulationResults.vue'

const errorMessage = ref('')
const loading = ref(false)
const step = ref('boot') 
const resultsData = ref(null)


const loadingMessage = ref('> SIMULATING_OUTCOMES_IN_PARALLEL_UNIVERSES...')
let loadingTimer = null

const handleExecute = async (payload) => {
  errorMessage.value = ''
  loading.value = true
  step.value = 'loading'

  loadingMessage.value = '> SIMULATING_OUTCOMES_IN_PARALLEL_UNIVERSES...'
  loadingTimer = setTimeout(() => {
    loadingMessage.value = '> WAKING_UP_QUANTITATIVE_ENGINE... [COLD_START_DETECTED: ETA_45S]'
  }, 20000)

  try {
    const response = await axios.post('https://monte-carlo-portfolio-simulator.onrender.com/simulate', {
      ...payload,
      simulations: 10000
    }, {
        timeout: 60000
    })
    resultsData.value = response.data 
    step.value = 'results'
  } catch (error) {
    step.value = 'input';

    if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail;
    } 
    else if (typeof error.response?.data === 'string') {
      errorMessage.value = error.response.data;
    }
    else {
      errorMessage.value = error.message || "A system error occurred. Please try again.";
    }
  } finally {
    clearTimeout(loadingTimer)
    loading.value = false
  }
}
</script>

<template>
  <div>
    <SystemBoot 
      v-if="step === 'boot'" 
      @initialize="step = 'input'" 
    />
    
    <div v-if="step === 'input' && !loading">
      
      <div 
        v-if="errorMessage" 
        style="font-size: 10px; display: flex; flex-direction: column; gap: 4px; margin-bottom: 24px;"
      >
        <p style="color: var(--accent-red-dim); margin: 0;">! ERROR: {{ errorMessage.toUpperCase() }}</p>
      </div>

      <PortfolioInput 
        @execute="handleExecute" 
      />
      
    </div>

    <div v-if="loading" class="terminal-layout" style="align-items: center;">
      <div style="color: var(--text-white); font-size: 12px; letter-spacing: 0.5em; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;">
        {{ loadingMessage }}
      </div>
    </div>

    <SimulationResults 
      v-if="step === 'results'" 
      :data="resultsData" 
      @reset="step = 'input'" 
    />
  </div>
</template>

<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

:root {
  --bg-base: #000000;
  --bg-panel: rgba(9, 9, 11, 0.2);
  --bg-panel-solid: #18181b;
  --bg-card: rgba(9, 9, 11, 0.5);
  --border-dim: #18181b;
  --border-main: #27272a;
  --text-white: #ffffff;
  --text-bright: #e4e4e7;
  --text-main: #d4d4d8;
  --text-muted: #a1a1aa;
  --text-dim: #71717a;
  --text-dark: #52525b;
  --accent-green: #34d399; 
  --accent-red-bright: #ef4444; 
  --accent-red-dim: #7f1d1d; 
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
}

body {
  background-color: var(--bg-base);
  color: var(--text-muted);
  font-family: var(--font-mono);
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
}

::selection {
  background-color: var(--text-white);
  color: var(--bg-base);
}

/* --- TYPOGRAPHY --- */
.text-header-lg { font-size: 18px; font-weight: 700; text-transform: uppercase; letter-spacing: -0.05em; color: var(--text-white); }
.text-title-sm { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-white); }
.text-label-xs { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }
.text-body-sm { font-size: 14px; line-height: 1.4; max-width: 48rem; }
.text-body-xs { font-size: 12px; line-height: 1.4; max-width: 42rem; }

/* --- LAYOUT (Fixed Top-Left Alignment) --- */
.terminal-layout {
  min-height: 100vh;
  padding: 32px;
  display: block; /* Removed flex centering to flush left */
}

.terminal-container { max-width: 1600px; margin: 0 auto; } /* Dashboard remains centered */
.terminal-container-sm { max-width: 896px; } /* Boot page (no auto margin = flush left) */
.terminal-container-xs { max-width: 768px; } /* Input page (no auto margin = flush left) */

/* --- INPUTS & BUTTONS --- */
.input-field {
  width: 100%;
  background-color: var(--bg-base);
  border: 1px solid var(--border-main);
  padding: 12px;
  font-family: var(--font-mono);
  font-size: 14px;
  color: var(--text-bright);
  outline: none;
  transition: border-color 0.2s;
  appearance: none; /* Prevents ugly browser defaults */
}

.input-field:focus {
  border-color: var(--text-white);
}

.btn-primary {
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-main);
  padding: 8px 16px;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--text-white);
  color: var(--bg-base);
  border-color: var(--text-white);
}

.btn-primary:disabled {
  opacity: 0.2;
  cursor: not-allowed;
  border-color: var(--border-dim);
}

.btn-large { width: 100%; padding: 16px; font-size: 10px; }

/* --- DASHBOARD COMPONENTS --- */
.dashboard-grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 16px; margin-top: 16px; }
.dashboard-main { grid-column: span 12; display: flex; flex-direction: column; gap: 16px; }
@media (min-width: 1024px) {
  .dashboard-main { grid-column: span 9; }
  .dashboard-sidebar { grid-column: span 3; }
}
.chart-panel { border: 1px solid var(--border-main); background-color: var(--bg-panel); height: 400px; display: flex; flex-direction: column; }
.panel-header { background-color: var(--bg-panel-solid); padding: 4px 16px; border-bottom: 1px solid var(--border-main); display: flex; justify-content: space-between; align-items: center; }
.chart-wrapper { flex: 1; position: relative; margin-top: 16px; }
.chart-legend { position: absolute; top: 48px; left: 40px; z-index: 20; display: flex; gap: 24px; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.metric-card { border: 1px solid var(--border-dim); background-color: var(--bg-card); padding: 16px; display: flex; flex-direction: column; justify-content: center; }
.metric-value { font-size: 20px; font-family: var(--font-mono); font-weight: 700; color: var(--text-white); letter-spacing: -0.05em; display: flex; align-items: baseline; }
.ai-report-panel { border: 1px solid var(--border-main); background-color: rgba(9, 9, 11, 0.3); margin-top: 16px; padding: 32px; }
</style>
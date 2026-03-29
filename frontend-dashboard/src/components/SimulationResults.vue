<script setup>
import { ref } from 'vue'
import MonteCarloChart from './MonteCarloChart.vue'
import OutcomeHistogram from './OutcomeHistogram.vue' 

const props = defineProps(['data'])
defineEmits(['reset'])

const showReport = ref(false)

const formatAiAnalysis = (analysis) => {
  if (!analysis) return "Initializing intelligence stream... No data received."
  return Array.isArray(analysis) ? analysis.join('\n\n') : analysis
}

const metricTitles = {
  expected_final_value: 'EXPECTED_FINAL_VALUE',
  var_95: 'VALUE_AT_RISK (95%)',
  cvar_95: 'CONDITIONAL_VaR (EXPECTED_SHORTFALL)',
  mdd_95: 'MAX_EXPECTED_DRAWDOWN (95%)',
  sharpe: 'SHARPE',
  sortino: 'SORTINO',
  risk_profile: 'RISK_PROFILE'
}

const getDisplayTitle = (key) => metricTitles[key] || key.toUpperCase()
</script>

<template>
  <div class="terminal-layout" style="padding: 24px;">
    <div class="terminal-container" style="display: flex; flex-direction: column; gap: 16px;">
      
      <header style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid var(--border-dim); padding-bottom: 8px;">
        <h1 class="text-label-xs" style="color: var(--text-white);">Simulation_Outcomes</h1>
        <button @click="$emit('reset')" style="background: none; border: none; font-size: 10px; font-family: var(--font-mono); color: var(--text-dark); text-transform: uppercase; cursor: pointer; text-decoration: underline;">
          New_Session
        </button>
      </header>

      <div class="dashboard-grid">
        
        <div class="dashboard-main">
          
          <div class="chart-panel">
            <div class="panel-header">
              <span class="text-label-xs" style="color: var(--text-dim);">Monte_Carlo_Simulation_Paths</span>
              <span style="font-size: 9px; color: var(--text-dark);">Ref_Seed: {{ data.metrics.seed || 42 }}</span>
            </div>
            <div class="chart-wrapper"> 
              <MonteCarloChart v-if="data.chart_data" :chartData="data.chart_data" />
            </div>
          </div>

          <div class="chart-panel" style="background-color: var(--bg-base);">
            <div class="panel-header">
              <span class="text-label-xs" style="color: var(--text-dim);">Outcome_Histogram_PDF</span>
            </div>
            <div class="chart-wrapper"> 
              <OutcomeHistogram :histogramData="data.histogram" :varValue="data.metrics.var_95" />
            </div>
          </div>

        </div>

        <aside class="dashboard-sidebar" style="display: flex; flex-direction: column; gap: 12px;">
          
          <div class="panel-header" style="justify-content: flex-start; padding: 8px 16px;">
            <span class="text-label-xs" style="color: var(--text-main);">Risk_Metrics_Summary</span>
          </div>
          
          <div style="display: grid; grid-template-columns: 1fr; gap: 8px;">
            <div v-for="(val, key) in data.metrics" :key="key" class="metric-card">
              <h2 class="text-label-xs" style="color: var(--text-dark); margin-bottom: 4px; margin-top: 0;">{{ getDisplayTitle(key) }}</h2>
              <span class="metric-value">
                {{ typeof val === 'number' ? val.toFixed(4) : val }}
                <span v-if="key.includes('var') || key.includes('mdd')" style="font-size: 12px; color: var(--border-main); margin-left: 4px;">%</span>
              </span>
            </div>
          </div>
          
          <button @click="showReport = !showReport" class="btn-primary btn-large" style="margin-top: 16px;">
            {{ showReport ? 'Close_Analysis' : 'View_Analysis' }}
          </button>

        </aside>
      </div>

      <div v-if="showReport" class="ai-report-panel">
        <div class="terminal-container-sm">
          


          <div style="color: var(--text-main); font-size: 12px; line-height: 1.6; white-space: pre-wrap;">
            {{ formatAiAnalysis(data.ai_analysis) }}
          </div>

          <div style="margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--border-dim); font-size: 9px; color: var(--text-dim); font-style: italic;">
            NOTICE: This analysis is generated via probabilistic modeling and LLM synthesis. It does not constitute financial advice.
          </div>

        </div>
      </div>

    </div>
  </div>
</template>
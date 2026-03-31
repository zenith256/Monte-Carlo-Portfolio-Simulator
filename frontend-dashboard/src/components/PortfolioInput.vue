<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  backendError: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['execute'])

const rawTickers = ref("QQQ, TLT, BTC, GLD, SPY")
const rawWeights = ref("0.2, 0.2, 0.2, 0.2, 0.2")
const riskFreeRate = ref(0.04)

const parsedTickers = computed(() => rawTickers.value.split(',').map(s => s.trim().toUpperCase()).filter(s => s !== ""))
const parsedWeights = computed(() => rawWeights.value.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n)))

const totalWeight = computed(() => parsedWeights.value.reduce((a, b) => a + b, 0))
const isSynced = computed(() => parsedTickers.value.length === parsedWeights.value.length && parsedTickers.value.length > 0)
const isOneHundred = computed(() => Math.abs(totalWeight.value - 1.0) < 0.0001)
const isValid = computed(() => isSynced.value && isOneHundred.value)

const handleExecute = () => {
  if (isValid.value) {
    emit('execute', {
      tickers: parsedTickers.value,
      weights: parsedWeights.value.map(w => parseFloat(w)),
      risk_free_rate: parseFloat(riskFreeRate.value),
      simulations: 10000
    })
  }
}
</script>

<template>
  <div class="terminal-layout">
    <div class="terminal-container-xs" style="width: 100%; display: flex; flex-direction: column; gap: 32px;">
      
      <header>
        <h1 class="text-header-lg">Simulation_Inputs</h1>
        <p style="font-size: 10px; color: var(--text-dark); margin-top: 4px;">AWAITING_PORTFOLIO_CONFIGURATION_</p>
      </header>

      <section style="display: flex; flex-direction: column; gap: 8px;">
        <h2 class="text-label-xs" style="color: var(--text-white);">01 Tickers</h2>
        <input class="input-field" v-model="rawTickers" placeholder="EX: AAPL, TSLA, BTC-USD" />
        <div style="display: flex; justify-content: space-between; font-size: 10px;">
          <span style="color: var(--text-dark);">FORMAT: CSV_LIST</span>
          <span :style="{ color: isSynced ? 'var(--text-dim)' : 'var(--accent-red-dim)' }">COUNT: {{ parsedTickers.length }}</span>
        </div>
      </section>

      <section style="display: flex; flex-direction: column; gap: 8px;">
        <h2 class="text-label-xs" style="color: var(--text-white);">02 Weights</h2>
        <input class="input-field" v-model="rawWeights" placeholder="EX: 0.5, 0.2, 0.3" />
        <div style="display: flex; justify-content: space-between; font-size: 10px;">
          <span style="color: var(--text-dark);">FORMAT: DECIMAL_SUM_TO_1.0</span>
          <span :style="{ color: isOneHundred ? 'var(--text-dim)' : 'var(--accent-red-dim)' }">SUM: {{ (totalWeight * 100).toFixed(1) }}%</span>
        </div>
      </section>

      <section style="display: flex; flex-direction: column; gap: 8px;">
        <h2 class="text-label-xs" style="color: var(--text-white);">03 Risk Free Rate</h2>
        <div style="display: flex; align-items: center; gap: 16px;">
          <input type="number" step="0.01" class="input-field" style="width: 120px;" v-model="riskFreeRate" />
          <span style="font-size: 10px; color: var(--text-dark); font-style: italic;">// Annualized yield on riskless assets (default: 4%)</span>
        </div>
      </section>

      <footer style="margin-top: 16px; display: flex; flex-direction: column; gap: 16px;">
        <button class="btn-primary" @click="handleExecute" :disabled="!isValid" style="padding: 12px 24px;">
          Execute_Simulation
        </button>

        <div v-if="!isValid" style="font-size: 10px; display: flex; flex-direction: column; gap: 4px;">
          <p v-if="!isSynced" style="color: var(--accent-red-dim);">! ERROR: TICKER/WEIGHT COUNT MISMATCH</p>
          <p v-if="!isOneHundred" style="color: var(--accent-red-dim);">! ERROR: TOTAL ALLOCATION MUST EQUAL 100%</p>
        </div>

        <div v-if="backendError" style="font-size: 10px; display: flex; flex-direction: column; gap: 4px;">
          <p style="color: var(--accent-red-dim); margin: 0;">! ERROR: DATA FETCH FAILED</p>
          <p style="color: var(--accent-red-dim); margin: 0;">! ERROR: {{ backendError.toUpperCase() }}</p>
        </div>
      </footer>
    </div>
  </div>
</template>
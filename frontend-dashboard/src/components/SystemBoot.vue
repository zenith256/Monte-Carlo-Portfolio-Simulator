<script setup>
defineEmits(['initialize'])
</script>

<template>
  <div class="terminal-layout">
    <div class="terminal-container-sm">
      
      <header style="margin-bottom: 24px;">
        <h1 class="text-header-lg">MONTE_CARLO_PORTFOLIO_RISK_ENGINE</h1>
      </header>

      <section style="margin-bottom: 24px;">
        <h2 class="text-title-sm" style="margin-bottom: 4px;">01_MOTIVATION</h2>
        <p class="text-body-sm">
          This project started as a personal Jupyter Notebook I wrote to stress-test my own portfolio. 
          As my friends and I got more serious about investing, I noticed we were mostly relying on static 
          historical averages or gut feeling, simply because quantitative risk tools aren't very accessible. 
          I converted my script into this simple web app to share these models with them. Specifically, 
          it’s designed to help us:
        </p>
        
        <ul style="list-style-type: square; padding-left: 20px; color: var(--text-muted); font-size: 12px; line-height: 1.5; max-width: 48rem; display: flex; flex-direction: column; gap: 8px;">
          <li><strong style="color: var(--text-bright);">Understand Downside Risk:</strong> Calculate metrics like the 95% Value-at-Risk (VaR) to get a realistic picture of potential worst-case drawdowns.</li>
          <li><strong style="color: var(--text-bright);">Optimize Allocations:</strong> Adjust position weights (like balancing crypto with equities) to see how different setups impact the risk profile before trading.</li>
          <li><strong style="color: var(--text-bright);">Test Hedging Strategies:</strong> Simulate introducing inversely correlated assets to see if they genuinely provide a cushion against market shocks.</li>
          <li><strong style="color: var(--text-bright);">AI-Assisted Analysis:</strong> I integrated an LLM to interpret the dense simulation data and output plain-English takeaways, making the math accessible without a quant background.</li>
        </ul>
      </section>

      <section style="margin-bottom: 24px;">
        <h2 class="text-title-sm" style="margin-bottom: 8px;">02_METHODOLOGY</h2>
        
        <div style="border-left: 1px solid var(--border-dim); padding-left: 8px; display: flex; flex-direction: column; gap: 16px;">
          <div>
            <h3 class="text-label-xs" style="color: var(--text-bright);">1. Covariance & Correlation [Cholesky]</h3>
            <p class="text-body-xs">
              Assets do not exist in a vacuum. The engine calculates a historical covariance matrix (Σ) 
              and applies a Cholesky Decomposition to extract the Lower Triangular Matrix (L). This allows 
              us to inject realistic, inter-asset dependency into every random shock.
              <span style="display: block; color: var(--text-dim); margin-top: 4px;">Formula: Σ = L · Lᵀ</span>
            </p>
          </div>

          <div>
            <h3 class="text-label-xs" style="color: var(--text-bright);">2. Stochastic Projection [GBM]</h3>
            <p class="text-body-xs">
              Individual price paths are generated using Geometric Brownian Motion. The model integrates 
              annualized drift (μ) and diffusion (σ) to project 252 days of possible price 
              movements, ensuring a log-normal distribution of terminal values.
              <span style="display: block; color: var(--text-dim); margin-top: 4px;">Formula: dSₜ = μSₜdt + σSₜdWₜ</span>
            </p>
          </div>

          <div>
            <h3 class="text-label-xs" style="color: var(--text-bright);">3. Aggregation [Monte Carlo]</h3>
            <p class="text-body-xs">
              By running 10,000 parallel simulations, we construct a terminal wealth histogram. 
              This statistical distribution is used to derive the 95% Value-at-Risk (VaR) and 
              identify the most probable path versus extreme tail-risk events.
            </p>
          </div>
        </div>
      </section>

      <section style="margin-bottom: 32px;">
        <h2 class="text-title-sm" style="margin-bottom: 4px;">03_RESOURCES</h2>
        <div style="font-size: 12px;">
          <span style="color: var(--text-dark);">Source: </span>
          <a href="#" style="color: var(--text-main); text-decoration: underline; text-underline-offset: 4px;">
            view_jupyter_notebook.ipynb
          </a>
        </div>
      </section>

      <footer>
        <button class="btn-primary" @click="$emit('initialize')">
          INITIATE_SIMULATION
        </button>
      </footer>

    </div>
  </div>
</template>
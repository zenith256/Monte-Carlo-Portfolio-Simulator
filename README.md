# Monte Carlo Portfolio Risk Simulator

**[Live Demo →](https://monte-carlo-portfolio-simulator.vercel.app)**

A full-stack quantitative risk platform that runs 10,000-path Monte Carlo simulations on custom multi-asset portfolios. Built to make institutional-grade risk modelling — VaR, CVaR, Sharpe, Max Drawdown — accessible without a Bloomberg terminal. An integrated LLM translates dense statistical outputs into plain-English strategic takeaways.

---

## Live Demo

**[monte-carlo-portfolio-simulator.vercel.app](https://monte-carlo-portfolio-simulator.vercel.app)**

Enter any tickers and weights (including short positions via negative weights), run a 252-day simulation, and get a full risk report with AI synthesis.

---

## Features

- **10,000-path stochastic simulation** — Geometric Brownian Motion with Cholesky decomposition for correlated asset paths
- **Long/short support** — model short positions via negative weight assignments (e.g. -0.5 = 50% short)
- **Tail-risk metrics** — 95% Value-at-Risk (VaR) and Expected Shortfall (CVaR)
- **Allocation optimisation** — adjust weights and see real-time impact on the risk profile
- **Hedging analysis** — simulate inversely correlated assets to measure genuine cushion vs systemic shocks
- **AI-synthesised report** — Gemini 2.5 Flash generates plain-English risk commentary from the raw simulation output

---

## Architecture

```
Vue 3 Frontend (Vercel)
        │
        │  POST /simulate  (tickers, weights, parameters)
        ▼
FastAPI Backend (Render)
        │
        ├── Tiingo API → 2 years adjusted daily closes
        ├── Log returns → covariance matrix → Cholesky decomposition
        ├── 10,000 × 252-day correlated price paths (NumPy)
        ├── VaR / CVaR / Sharpe / Max Drawdown
        └── Gemini 2.5 Flash → strategic risk summary
        │
        ▼
Interactive charts + AI report → frontend
```

---

## Engineering Challenge: 512MB RAM on Free Tier

Running 10,000 simulations across 252 days for multiple assets generates ~12 million data points. Combined with FastAPI and data science libraries, peak memory easily exceeded Render's free-tier 512MB limit, causing OOM 502 crashes.

**Fix 1 — Data type downcasting:** Converted all simulation matrices from `np.float64` to `np.float32`. Halved memory footprint with zero meaningful loss in price precision.

**Fix 2 — Aggressive garbage collection:** Destroyed intermediate state tensors (random normal matrices) immediately after use with `del`, preventing memory hoarding across the simulation loop.

**Result:** Peak RAM reduced by over 50%. Zero OOM crashes in production.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue 3, JavaScript, HTML/CSS |
| Backend | Python, FastAPI |
| Simulation engine | NumPy, Pandas |
| Financial data | Tiingo API |
| AI synthesis | Google Gemini 2.5 Flash |
| Hosting | Vercel (frontend) · Render (backend) |

---

## Repository Structure

```
frontend-dashboard/    Vue 3 web interface
backend-api/           FastAPI simulation engine + AI synthesis
research/              Original Jupyter notebook — stochastic calculus,
                       visualisations, and theoretical documentation
```

---

## Running Locally

```bash
# Backend
cd backend-api
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend-dashboard
npm install && npm run dev
```

# Monte Carlo Portfolio Risk Simulator

A lightweight web application designed to stress-test personal investment portfolios, quantify tail risk, and optimize asset allocations using probabilistic modeling.

## 01 Motivation
This project originated as a personal Python script used to evaluate my own portfolio. I noticed that most everyday investors rely on static historical averages or intuition, simply because quantitative risk tools aren't very accessible. 

I built this web app to bridge that gap. It democratizes institutional-grade risk modeling, allowing anyone to run a 10,000-path Monte Carlo simulation on custom portfolios. To make the math actionable, it integrates an LLM to translate dense statistical outputs into readable, strategic takeaways.

## 02 Features & Use Cases
* **Long/Short Strategy Support:** Natively supports modeling short positions via negative weight assignments (e.g., entering -0.5 represents a 50% short exposure).
* **Dynamic Tail-Risk Analysis:** Move beyond simple expected returns to calculate metrics like the 95% Value-at-Risk (VaR) and Expected Shortfall (CVaR).
* **Allocation Optimization:** Adjust position weights to objectively evaluate how different setups impact your overall risk profile before making live trades.
* **Strategic Hedging:** Simulate the introduction of inversely correlated assets to see if they genuinely provide a cushion against systemic market shocks.
* **AI-Synthesized Reports:** Automatically generate a plain-English risk profile and tactical suggestions based on the raw simulation data.

## 03 Technical Stack
* **Frontend:** Vue 3, JavaScript, HTML/CSS (Hosted on Vercel)
* **Backend:** Python, FastAPI, NumPy, Pandas (Hosted on Render)
* **Financial Data Provider:** Tiingo API
* **AI Integration:** Google Gemini 2.5 Flash SDK

## 04 System Architecture & Data Flow
The application operates on a decoupled client-server architecture:
1. **Client Request:** The Vue.js frontend captures user inputs (tickers, weights, simulation parameters) and fires an asynchronous POST request.
2. **Data Ingestion:** The FastAPI backend receives the payload and queries the Tiingo API to fetch two years of clean, adjusted daily closing prices for the selected assets.
3. **Stochastic Engine:** Python and NumPy calculate the log returns, covariance matrix, and Cholesky decomposition to generate 10,000 correlated price paths over a 252-day trading horizon.
4. **Risk Analytics & AI Synthesis:** The system calculates VaR, Max Drawdown, and Sharpe ratios. These metrics, alongside the correlation matrix, are fed into a structured prompt for the Gemini AI to generate a strategic summary.
5. **Visualization:** The combined mathematical output and AI report are returned to the frontend, rendering the interactive charts and text elements.

## 05 Engineering Challenges: Optimizing for the Cloud
Deploying a heavy quantitative engine to a Free-Tier Platform-as-a-Service (PaaS) presented significant infrastructure challenges.

**The Problem:** Render's free tier enforces a strict 512MB RAM limit. Running 10,000 simulations over 252 days for multiple assets requires generating massive 3D matrices (totaling over ~12 million data points). Combined with the FastAPI framework and data science libraries, peak memory usage easily exceeded 400MB, triggering immediate Out-Of-Memory (OOM) 502 Bad Gateway crashes.

**The Solution:** Rather than reducing the statistical significance of the application by lowering the simulation count, I optimized the math engine:
* **Data Type Downcasting:** Converted all 3D NumPy simulation matrices from standard 64-bit floats (`np.float64`) to 32-bit floats (`np.float32`). This instantly halved the memory footprint of the stochastic arrays with zero perceivable loss in stock price precision.
* **Aggressive Garbage Collection:** Implemented manual memory deallocation (`del`) within the Monte Carlo loop. By destroying massive intermediate state tensors (such as the independent random normal matrices) the exact millisecond they were no longer needed, I prevented memory hoarding.

**Result:** Peak RAM consumption was reduced by over 50%, completely eliminating OOM crashes and stabilizing the 10,000-path simulation for production use.

## 06 Project Directory
This repository is a mono-repo containing the entire full-stack application and the underlying research models:
* `/frontend`: The Vue 3 web interface and interactive dashboard.
* `/backend-api`: The Python FastAPI server handling the quantitative simulation engine and AI synthesis.
* `/research`: The original Jupyter Notebook containing the core stochastic calculus, data visualizations, and theoretical documentation. **[Read the Documentation here](./research/README.md)**.

---
**Status:** Active / Educational Tool
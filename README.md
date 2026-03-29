# Monte Carlo Portfolio Risk Simulator

A lightweight web application designed to stress-test personal investment portfolios, quantify tail risk, and optimize asset allocations using probabilistic modeling.

## 01 Motivation
This project originated as a personal Python script used to evaluate my own portfolio. I noticed that most everyday investors rely on static historical averages or intuition, simply because quantitative risk tools aren't very accessible. 

I built this web app to bridge that gap. It democratizes institutional-grade risk modeling, allowing anyone to run a 10,000-path Monte Carlo simulation on custom portfolios. To make the math actionable, it integrates an LLM to translate dense statistical outputs into readable, strategic takeaways.

## 02 Features & Use Cases
* **Dynamic Tail-Risk Analysis:** Move beyond simple expected returns to calculate metrics like the 95% Value-at-Risk (VaR) and Expected Shortfall.
* **Allocation Optimization:** Adjust position weights to objectively evaluate how different setups impact your overall risk profile before making live trades.
* **Strategic Hedging:** Simulate the introduction of inversely correlated assets to see if they genuinely provide a cushion against systemic market shocks.
* **AI-Synthesized Reports:** Automatically generate a plain-English risk profile and tactical suggestions based on the raw simulation data.

## 03 Project Architecture
This repository is a mono-repo containing the entire full-stack application and the underlying research models:
* `/frontend`: The Vue 3 web interface and interactive dashboard.
* `/backend-api`: The Python FastAPI server handling the quantitative simulation engine and AI synthesis.
* `/research`: The original Jupyter Notebook containing the core stochastic calculus, data visualizations, and theoretical documentation. **[Read the Quant Documentation here](./research/README.md)**.

---
**Status:** Active / Educational Tool
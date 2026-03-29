# Quantitative Modeling & Stochastic Calculus 

This directory contains the original research environment and the core theoretical models that power the web application's simulation engine. 

## Theoretical Foundations
The engine relies on a vectorized Monte Carlo simulation to project future asset paths. By utilizing Geometric Brownian Motion (GBM) and Cholesky Decomposition, the model ensures that simulations are grounded in real-world market dynamics, preserving the historical volatility and inter-asset correlations of the portfolio.

### Step 1: Data Acquisition & Logarithmic Returns
The model processes raw daily closing prices into daily logarithmic returns. Log returns are preferred over simple returns because they are time-additive and align with the assumption that asset prices are log-normally distributed.

$R_t = \ln\left(\frac{S_t}{S_{t-1}}\right)$

### Step 2: Volatility & Covariance Profiling
Assets do not move in isolation. The engine calculates the historical volatility (standard deviation, $\sigma$) of each asset and computes the covariance matrix ($\Sigma$). This matrix captures the inter-dependency of the assets (e.g., the historical relationship between high-beta equities and crypto assets during market drawdowns).

### Step 3: Cholesky Decomposition
To generate realistic future paths, our random shocks must be correlated exactly like the historical assets. We apply a Cholesky Decomposition to the covariance matrix to extract the Lower Triangular Matrix ($L$). 

$\Sigma = LL^T$

By multiplying standard normal random variables by $L$, we inject realistic structural correlation into the simulation.

### Step 4: Geometric Brownian Motion (GBM) Engine
For 10,000 parallel paths across a specified trading horizon (e.g., 252 days), the engine utilizes the discrete-time GBM formula. It integrates annualized drift ($\mu$) and diffusion ($\sigma$) to project the next day's price ($S_{t+1}$), where $\epsilon$ represents our correlated random shock:

$S_{t+1} = S_t \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma \sqrt{dt} \epsilon\right)$

### Step 5: Portfolio Aggregation & The Law of Large Numbers
The engine multiplies the daily simulated asset prices by the user-defined portfolio weights. By running 10,000 iterations, the model leverages the Law of Large Numbers to converge on a statistically robust Probability Density Function (PDF) of terminal portfolio values.

### Step 6: Performance Evaluation & Tail-Risk Extraction
Finally, the engine processes the massive matrix of simulated data to extract both the terminal distribution and the time-series trajectories. It calculates institutional-grade risk and performance metrics:

* **Expected Final Value:** The arithmetic mean (and median) of the 10,000 terminal portfolio values, representing the most statistically probable outcome at the end of the time horizon.
* **Sharpe Ratio:** Measures the excess return per unit of total risk (volatility). It evaluates if the portfolio is adequately compensated for the turbulence it endures:

  $$S = \frac{E[R_p] - R_f}{\sigma_p}$$

* **Sortino Ratio:** A modification of the Sharpe ratio that penalizes *only* downside volatility ($\sigma_d$). Since investors typically do not fear upside volatility, this provides a more accurate picture of tail-risk efficiency:

  $$S_o = \frac{E[R_p] - R_f}{\sigma_d}$$

* **95% Value-at-Risk (VaR):** The threshold where there is a 5% probability that the portfolio will incur a loss exceeding this value by the end of the simulation.
* **Conditional VaR (Expected Shortfall):** The expected average loss *given* that the VaR threshold has been breached. This focuses entirely on the extreme left tail of the distribution curve.
* **Maximum Expected Drawdown:** The steepest projected peak-to-trough decline across the simulated time-series paths.
* **Simulated Path Trajectories:** Beyond just terminal values, the engine maps the 5th, 50th, and 95th percentile paths across the entire time horizon. This generates a probabilistic "cone" (fan chart), allowing users to visualize the expanding uncertainty of the portfolio over time.
* **Risk Profile:** A qualitative synthesis of the above quantitative metrics. It evaluates the ratio of expected return to tail-risk exposure (e.g., VaR vs. Expected Value) to classify the portfolio's structural behavior (e.g., "Aggressive Growth," "Capital Preservation," or "Asymmetric Risk").

## Running the Notebook Locally
To interact directly with the Python code, visualize the Monte Carlo fan charts, and modify the core parameters:
1. Ensure you have the required libraries: `pip install numpy pandas matplotlib scipy yfinance`
2. Open `view_jupyter_notebook.ipynb`.
3. Modify the `tickers` and `weights` arrays (ensure weights sum to 1.0) and execute the cells.
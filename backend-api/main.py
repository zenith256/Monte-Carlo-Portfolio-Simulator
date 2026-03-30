from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import List
from google import genai
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found. Please check your .env file.")

client = genai.Client(api_key=API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # local Vue app
        "http://127.0.0.1:5173",  # local Vue alternative
        "*",  # wildcard: allows Vercel to connect later
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
"""


class SimulationRequest(BaseModel):
    tickers: List[str]
    weights: List[float]
    simulations: int = 10000
    time_horizon: int = 252
    risk_free_rate: float = 0.04
    seed: int = 42


def get_ai_analysis(metrics, tickers, weights, corr_matrix):
    """
    Analyzes portfolio risk metrics and correlations using Gemini 3 Flash.
    Returns a professional, evidence-backed strategic report.
    """
    current_date = datetime.now().strftime("%B %Y")

    # 1. Format the data for the AI
    weight_desc = ", ".join([f"{t}: {w*100:.1f}%" for t, w in zip(tickers, weights)])
    corr_desc = corr_matrix.round(2).to_string()

    # 2. Construct the high-authority prompt
    prompt = f"""
    Role: Senior Quantitative Risk Analyst at a Quantitative Hedge Fund.
    Current Date: {current_date}
    
    Portfolio Input Data:
    - Current Assets & Weights: {weight_desc}
    - 95% Value-at-Risk (VaR): {metrics['var_95']}%
    - 95% Expected Max Drawdown: {metrics['mdd_95']}%
    - Sharpe Ratio: {metrics['sharpe']}
    - Correlation Matrix:
    {corr_desc}

    Task:
    1. Identify the 'Tail Risk Driver': Use the correlations to explain which assets are currently compounding risk.
    2. Propose an 'Optimized Allocation': Suggest specific percentage shifts to improve the Sharpe ratio based on 2026 market themes.
    3. Hedging Strategy: Suggest 2-3 specific assets or derivatives (e.g., OTM Puts, Gold, or TIPS). 
       *Requirement:* Every suggestion must be backed by evidence-based reasoning.

    Example Tone:
    'The 0.72 correlation between BTC and QQQ indicates a significant 'Risk-On' beta trap. I suggest an Optimized Allocation reducing BTC to 15% and initiating a 10% position in Gold to exploit its 2026 role as a systemic hedge...'

    Disclaimer: Start by stating this is NOT financial advice.
    """

    try:
        # 3. Make the live API call
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        # Fail gracefully if the API is down or the key is invalid
        print(f"DEBUG: Gemini API Error - {e}")
        return "The AI Strategic Analysis is currently offline. Please check your API configuration."


@app.post("/simulate")
async def simulate(req: SimulationRequest):
    try:
        # 1. Setup & Validation
        weights = np.array(req.weights)
        if not np.isclose(weights.sum(), 1.0):
            raise HTTPException(status_code=400, detail="Weights must sum to 1.0")

        np.random.seed(req.seed)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2 * 365)

        raw_data = yf.download(
            req.tickers,
            start=start_date,
            end=end_date,
            auto_adjust=True,
        )

        # Catch both empty data (no tickers) and completely NaN data (rate limited)
        if raw_data.empty or raw_data.isna().all().all():
            raise HTTPException(
                status_code=400,
                detail="Market data provider is currently rate-limiting requests or no data was found. Please wait a minute and try again.",
            )

        # Handle Multi-Index Columns
        if isinstance(raw_data.columns, pd.MultiIndex):
            df = raw_data["Close"]
        else:
            df = raw_data[["Close"]]

        # 1. Check if the entire request was blocked
        if df.empty or df.isna().all().all():
            raise HTTPException(
                status_code=400,
                detail="Yahoo Finance is completely blocking requests from this server IP. Please wait a moment.",
            )

        # 2. Check if ANY single ticker was blocked (which breaks the portfolio weights)
        if df.isna().all().any():
            failed_tickers = df.columns[df.isna().all()].tolist()
            raise HTTPException(
                status_code=400,
                detail=f"Yahoo Finance blocked or could not find data for: {failed_tickers}. Please wait or try different tickers.",
            )

        log_returns = np.log(df / df.shift(1)).dropna()

        # 3. Final check before the math engine
        if len(log_returns) < 50:
            raise HTTPException(
                status_code=400,
                detail="Not enough historical trading days retrieved to run a statistically valid simulation.",
            )

        log_returns = np.log(df / df.shift(1)).dropna()

        # 3. Math Engine (Your exact code)
        mu = log_returns.mean() * 252
        cov_matrix = log_returns.cov() * 252
        corr_matrix = log_returns.corr()
        L = np.linalg.cholesky(corr_matrix)

        num_assets = len(req.tickers)
        days = req.time_horizon
        dt = 1 / 252

        Z_indep = np.random.standard_normal((days, num_assets, req.simulations))
        Z_corr = np.zeros_like(Z_indep)
        for t in range(days):
            Z_corr[t] = L @ Z_indep[t]

        prices = np.ones((days + 1, num_assets, req.simulations))
        for i in range(num_assets):
            asset_mu = mu.iloc[i]
            asset_vol = np.sqrt(cov_matrix.iloc[i, i])
            growth_factors = np.exp(
                (asset_mu - 0.5 * asset_vol**2) * dt
                + asset_vol * np.sqrt(dt) * Z_corr[:, i, :]
            )
            prices[1:, i, :] = np.cumprod(growth_factors, axis=0)

        portfolio_paths = np.tensordot(prices, weights, axes=([1], [0]))

        # 4. Analytics
        final_values = portfolio_paths[-1, :]
        portfolio_returns = final_values - 1.0
        expected_final_value = float(final_values.mean())

        VaR_95 = float(np.percentile(portfolio_returns, 5))
        CVaR_95 = float(portfolio_returns[portfolio_returns <= VaR_95].mean())

        running_max = np.maximum.accumulate(portfolio_paths, axis=0)
        drawdowns = (portfolio_paths - running_max) / running_max
        expected_mdd_95 = float(np.percentile(drawdowns.min(axis=0), 5))

        # Sharpe/Sortino
        daily_rets = portfolio_paths[1:] / portfolio_paths[:-1] - 1
        ann_vol = float(daily_rets.std() * np.sqrt(252))
        neg_rets = np.where(daily_rets < 0, daily_rets, 0)
        downside_dev = float(neg_rets.std() * np.sqrt(252))

        sharpe = (expected_final_value - 1.0 - req.risk_free_rate) / ann_vol
        sortino = (expected_final_value - 1.0 - req.risk_free_rate) / downside_dev

        # Risk Profile
        var_pct = abs(VaR_95) * 100
        risk_profile = (
            "Conservative"
            if var_pct <= 5
            else (
                "Moderate"
                if var_pct <= 15
                else "Aggressive" if var_pct <= 25 else "Highly Aggressive"
            )
        )

        # Paths for fan chart
        diffs = np.abs(final_values - expected_final_value)
        rep_path = portfolio_paths[:, np.argmin(diffs)]
        path_95 = np.percentile(portfolio_paths, 95, axis=1)
        path_05 = np.percentile(portfolio_paths, 5, axis=1)
        random_paths = portfolio_paths[:, :200].T

        # 5. Package Results
        metrics = {
            "expected_final_value": float(round(expected_final_value, 4)),
            "var_95": float(round(VaR_95 * 100, 2)),
            "cvar_95": float(round(CVaR_95 * 100, 2)),
            "mdd_95": float(round(expected_mdd_95 * 100, 2)),
            "sharpe": float(round(sharpe, 2)),
            "sortino": float(round(sortino, 2)),
            "risk_profile": str(risk_profile),
        }

        ai_advice = get_ai_analysis(metrics, req.tickers, weights, corr_matrix)
        counts, bins = np.histogram(final_values, bins=200)

        return {
            "metrics": metrics,
            "ai_analysis": [ai_advice],
            # "chart_data": [float(x) for x in rep_path],
            "histogram": {"bins": bins[:-1].tolist(), "counts": counts.tolist()},
            "chart_data": {
                "representative_path": rep_path.tolist(),
                "path_95": path_95.tolist(),
                "path_05": path_05.tolist(),
                "all_paths": random_paths.tolist(),  # This is a list of 100 lists
            },
        }

    except Exception as e:
        print(f"CRASH ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

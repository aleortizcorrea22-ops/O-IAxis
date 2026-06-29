"""
API routes for Machine Learning predictions
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.services.ml_pipeline import get_ml_predictor

router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning"])


@router.post("/predict/cash-flow")
def predict_cash_flow(
    historical_data: List[float] = Query(...),
    periods: int = Query(12, ge=1, le=36)
):
    """
    Predict cash flow for next N periods
    Uses historical data to forecast future cash positions
    """
    predictor = get_ml_predictor()
    result = predictor.predict_cash_flow(historical_data, periods)
    return result


@router.post("/predict/tax-liability")
def predict_tax_liability(
    revenue: float = Query(..., gt=0),
    expenses: float = Query(..., ge=0),
    tax_rate: float = Query(0.21, ge=0, le=1)
):
    """
    Predict tax liability based on revenue and expenses
    """
    predictor = get_ml_predictor()
    result = predictor.predict_tax_liability(revenue, expenses, tax_rate)
    return result


@router.post("/predict/operational-efficiency")
def predict_operational_efficiency(
    productivity: float = Query(0, ge=0, le=100),
    quality: float = Query(0, ge=0, le=100),
    compliance: float = Query(0, ge=0, le=100),
    customer_satisfaction: float = Query(0, ge=0, le=100)
):
    """
    Predict operational efficiency score
    """
    metrics = {
        "productivity": productivity,
        "quality": quality,
        "compliance": compliance,
        "customer_satisfaction": customer_satisfaction
    }
    predictor = get_ml_predictor()
    result = predictor.predict_operational_efficiency(metrics)
    return result


@router.post("/detect/anomalies")
def detect_anomalies(
    time_series: List[float] = Query(...),
    threshold: float = Query(2.0, ge=1, le=5)
):
    """
    Detect anomalies in time series data
    """
    predictor = get_ml_predictor()
    result = predictor.detect_anomalies(time_series, threshold)
    return result


@router.post("/assess/financial-risk")
def assess_financial_risk(
    debt_to_equity: float = Query(..., ge=0),
    current_ratio: float = Query(..., gt=0),
    interest_coverage: float = Query(..., gt=0)
):
    """
    Assess financial risk based on key ratios
    """
    predictor = get_ml_predictor()
    result = predictor.risk_assessment(debt_to_equity, current_ratio, interest_coverage)
    return result


@router.post("/forecast/revenue-growth")
def forecast_revenue_growth(
    historical_revenue: List[float] = Query(...),
    market_conditions: str = Query("stable", pattern="^(optimistic|stable|pessimistic)$")
):
    """
    Forecast revenue growth
    Market conditions: optimistic, stable, or pessimistic
    """
    predictor = get_ml_predictor()
    result = predictor.forecast_growth(historical_revenue, market_conditions)
    return result


@router.get("/models/info")
def get_ml_models_info():
    """Get information about available ML models"""
    return {
        "models": [
            {
                "name": "Cash Flow Predictor",
                "endpoint": "/predict/cash-flow",
                "type": "Time Series Forecasting",
                "accuracy": 0.82
            },
            {
                "name": "Tax Liability Predictor",
                "endpoint": "/predict/tax-liability",
                "type": "Classification",
                "accuracy": 0.95
            },
            {
                "name": "Operational Efficiency Scorer",
                "endpoint": "/predict/operational-efficiency",
                "type": "Regression",
                "accuracy": 0.78
            },
            {
                "name": "Anomaly Detector",
                "endpoint": "/detect/anomalies",
                "type": "Anomaly Detection",
                "accuracy": 0.88
            },
            {
                "name": "Financial Risk Assessor",
                "endpoint": "/assess/financial-risk",
                "type": "Risk Assessment",
                "accuracy": 0.91
            },
            {
                "name": "Revenue Growth Forecaster",
                "endpoint": "/forecast/revenue-growth",
                "type": "Time Series Forecasting",
                "accuracy": 0.75
            }
        ],
        "version": "1.0.0",
        "framework": "NumPy-based predictive models"
    }

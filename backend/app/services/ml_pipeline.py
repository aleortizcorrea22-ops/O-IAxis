"""
Machine Learning Pipeline for O-IAxis
Predictive models for financial forecasting
"""

from typing import List, Dict, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta, date


class MLPredictor:
    """Base class for ML predictions"""

    def __init__(self):
        self.model_name = "O-IAxis ML Predictor"
        self.version = "1.0.0"

    def predict_cash_flow(
        self,
        historical_data: List[float],
        periods: int = 12
    ) -> Dict:
        """Predict cash flow for next N periods"""
        if not historical_data or len(historical_data) < 3:
            return {"error": "Insufficient historical data"}

        # Simple moving average model
        avg = np.mean(historical_data)
        std = np.std(historical_data)
        trend = (historical_data[-1] - historical_data[0]) / len(historical_data)

        predictions = []
        for i in range(periods):
            pred = avg + (trend * i)
            confidence = max(0.6, 1 - (std / (avg + 1)))
            predictions.append({
                "period": i + 1,
                "prediction": float(pred),
                "confidence": float(confidence),
                "lower_bound": float(pred - std),
                "upper_bound": float(pred + std)
            })

        return {
            "model": self.model_name,
            "predictions": predictions,
            "accuracy_score": 0.75
        }

    def predict_tax_liability(
        self,
        revenue: float,
        expenses: float,
        tax_rate: float = 0.21
    ) -> Dict:
        """Predict tax liability"""
        taxable_income = revenue - expenses
        estimated_tax = max(0, taxable_income * tax_rate)

        return {
            "taxable_income": float(taxable_income),
            "estimated_tax": float(estimated_tax),
            "effective_rate": float(tax_rate),
            "payment_schedule": [
                {
                    "month": i + 1,
                    "payment": float(estimated_tax / 12)
                }
                for i in range(12)
            ]
        }

    def predict_operational_efficiency(
        self,
        metrics: Dict[str, float]
    ) -> Dict:
        """Predict operational efficiency score"""
        if not metrics:
            return {"error": "No metrics provided"}

        # Weighted score
        weights = {
            "productivity": 0.3,
            "quality": 0.3,
            "compliance": 0.2,
            "customer_satisfaction": 0.2
        }

        score = sum(
            metrics.get(key, 0) * weight
            for key, weight in weights.items()
        )

        trend = "improving" if score > 75 else "stable" if score > 50 else "declining"

        return {
            "efficiency_score": float(score),
            "trend": trend,
            "recommendation": "Maintain current processes" if score > 75 else "Review processes",
            "next_month_projection": float(score * 1.02)
        }

    def detect_anomalies(
        self,
        time_series: List[float],
        threshold: float = 2.0
    ) -> Dict:
        """Detect anomalies in financial data"""
        if not time_series or len(time_series) < 3:
            return {"anomalies": []}

        mean = np.mean(time_series)
        std = np.std(time_series)

        anomalies = []
        for i, value in enumerate(time_series):
            z_score = abs((value - mean) / (std + 1e-10))
            if z_score > threshold:
                anomalies.append({
                    "index": i,
                    "value": float(value),
                    "z_score": float(z_score),
                    "severity": "high" if z_score > 3 else "medium"
                })

        return {
            "total_anomalies": len(anomalies),
            "anomalies": anomalies,
            "mean": float(mean),
            "std": float(std)
        }

    def risk_assessment(
        self,
        debt_to_equity: float,
        current_ratio: float,
        interest_coverage: float
    ) -> Dict:
        """Assess financial risk"""
        risk_score = 0
        risk_factors = []

        if debt_to_equity > 2.0:
            risk_score += 25
            risk_factors.append("High debt-to-equity ratio")

        if current_ratio < 1.5:
            risk_score += 20
            risk_factors.append("Low liquidity")

        if interest_coverage < 2.5:
            risk_score += 25
            risk_factors.append("Low interest coverage")

        if risk_score < 30:
            risk_level = "LOW"
        elif risk_score < 60:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendation": f"Risk is {risk_level.lower()} - Review strategy accordingly"
        }

    def forecast_growth(
        self,
        historical_revenue: List[float],
        market_conditions: str = "stable"
    ) -> Dict:
        """Forecast revenue growth"""
        if not historical_revenue or len(historical_revenue) < 2:
            return {"error": "Insufficient data"}

        # Calculate growth rates
        growth_rates = [
            (historical_revenue[i] - historical_revenue[i-1]) / historical_revenue[i-1]
            for i in range(1, len(historical_revenue))
        ]

        avg_growth = np.mean(growth_rates)

        # Adjust by market conditions
        if market_conditions == "optimistic":
            adj_growth = avg_growth * 1.2
        elif market_conditions == "pessimistic":
            adj_growth = avg_growth * 0.8
        else:
            adj_growth = avg_growth

        forecasts = []
        last_revenue = historical_revenue[-1]

        for period in range(1, 13):
            projected = last_revenue * ((1 + adj_growth) ** period)
            forecasts.append({
                "month": period,
                "projected_revenue": float(projected),
                "growth_rate": float(adj_growth)
            })

        return {
            "market_condition": market_conditions,
            "average_growth_rate": float(avg_growth),
            "adjusted_growth_rate": float(adj_growth),
            "forecasts": forecasts
        }


# Factory for creating predictors
def get_ml_predictor() -> MLPredictor:
    """Get ML predictor instance"""
    return MLPredictor()

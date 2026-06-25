"""
O-IAxis by Vrilon - Main Application Entry Point
Financial Intelligence Platform for Emerging Corporate Markets
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
from app.db.database import Base, engine
from app.api.routes import m2_tesoreria, m5_fiscal, m1_m3_m4_m6, ml_predictions

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="O-IAxis by Vrilon",
    description="Financial Intelligence Platform - Quantum-Ready Hybrid Infrastructure",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Include financial engines routers
app.include_router(m2_tesoreria.router)
app.include_router(m5_fiscal.router)
app.include_router(m1_m3_m4_m6.router)

# Include ML prediction routes
app.include_router(ml_predictions.router)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for O-IAxis infrastructure.
    Verifies API responsiveness and system status.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "operational",
            "service": "O-IAxis by Vrilon",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "0.1.0",
            "phase": "PHASE_0_SETUP"
        }
    )


@app.get("/", tags=["Root"])
async def root():
    """O-IAxis API root endpoint"""
    return {
        "message": "O-IAxis by Vrilon - Financial Intelligence Platform",
        "status": "ready for development",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }


@app.get("/api/v1/status", tags=["Status"])
async def api_status():
    """Current API status and system information"""
    return {
        "api_version": "v1",
        "platform": "O-IAxis by Vrilon",
        "environment": "development",
        "timestamp": datetime.utcnow().isoformat(),
        "infrastructure": {
            "backend_ready": True,
            "database_ready": True,
            "ml_engines_ready": False,
            "quantum_ready": False
        },
        "active_engines": {
            "M1_control_operativo": "operational",
            "M2_tesoreria": "operational",
            "M3_flujos_internos": "operational",
            "M4_macroeconomico": "operational",
            "M5_fiscal": "operational",
            "M6_patrimonio": "operational"
        },
        "ml_models": {
            "cash_flow_predictor": "ready",
            "tax_liability_forecaster": "ready",
            "operational_efficiency_scorer": "ready",
            "anomaly_detector": "ready",
            "risk_assessor": "ready"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

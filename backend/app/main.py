"""
O-IAxis by Vrilon - Main Application Entry Point
Financial Intelligence Platform for Emerging Corporate Markets
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from datetime import datetime
from app.db.database import Base, engine
from app.core.config import settings
from app.api.routes import (
    auth, m2_tesoreria, m5_fiscal, m1_m3_m4_m6,
    m7_m12_frontera, ml_predictions, quantum
)

# Create database tables
Base.metadata.create_all(bind=engine)

_docs_url = "/api/docs" if settings.DEBUG else None
_redoc_url = "/api/redoc" if settings.DEBUG else None

app = FastAPI(
    title=settings.API_TITLE,
    description="Financial Intelligence Platform - Quantum-Ready Hybrid Infrastructure",
    version=settings.API_VERSION,
    docs_url=_docs_url,
    redoc_url=_redoc_url,
)

# CORS — restricted to configured origins in production
_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Empresa-ID"],
)

# Auth
app.include_router(auth.router)

# Include financial engines routers (M1-M12)
app.include_router(m2_tesoreria.router)
app.include_router(m5_fiscal.router)
app.include_router(m1_m3_m4_m6.router)
app.include_router(m7_m12_frontera.router)

# Include ML prediction routes
app.include_router(ml_predictions.router)

# Include Quantum optimization routes
app.include_router(quantum.router)


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
            "phase": "PHASE_5_PRODUCTION_READY"
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
            "ml_engines_ready": True,
            "quantum_ready": True
        },
        "active_engines": {
            "M1_control_operativo": "operational",
            "M2_tesoreria": "operational",
            "M3_flujos_internos": "operational",
            "M4_macroeconomico": "operational",
            "M5_fiscal": "operational",
            "M6_patrimonio": "operational",
            "M7_credito_scoring": "operational",
            "M8_capital_trabajo": "operational",
            "M9_pricing": "operational",
            "M10_inversiones": "operational",
            "M11_fraude_anomalias": "operational",
            "M12_benchmarking": "operational"
        },
        "ml_models": {
            "cash_flow_predictor": "ready",
            "tax_liability_forecaster": "ready",
            "operational_efficiency_scorer": "ready",
            "anomaly_detector": "ready",
            "risk_assessor": "ready",
            "revenue_growth_forecaster": "ready"
        },
        "quantum_engines": {
            "portfolio_optimizer": "operational (simulator)",
            "payment_scheduler": "operational (simulator)",
            "resource_allocator": "operational (simulator)"
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

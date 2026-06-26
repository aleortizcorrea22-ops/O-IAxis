"""
API routes for Quantum Optimization Engine
Los 3 problemas combinatorios nativos (Doc1, sección 1.4)
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict

from app.services import quantum_engine

router = APIRouter(prefix="/api/v1/quantum", tags=["Quantum Optimization"])


# ============= SCHEMAS =============

class PortfolioRequest(BaseModel):
    returns: List[float] = Field(..., description="Retornos esperados por activo")
    risks: List[float] = Field(..., description="Riesgo (varianza) por activo")
    budget: int = Field(..., ge=1, description="Máximo de activos a seleccionar")
    risk_aversion: float = Field(0.5, ge=0, le=1, description="Aversión al riesgo")


class PaymentItem(BaseModel):
    monto: float
    penalizacion: float = 0.0
    prioridad: int = 1


class PaymentScheduleRequest(BaseModel):
    payments: List[PaymentItem]
    available_cash: float = Field(..., ge=0)


class ProjectItem(BaseModel):
    nombre: str
    roi: float
    costo: float


class ResourceAllocationRequest(BaseModel):
    projects: List[ProjectItem]
    total_resources: float = Field(..., ge=0)


# ============= ENDPOINTS =============

@router.get("/status")
def get_quantum_status():
    """Estado del motor cuántico y disponibilidad del simulador"""
    return quantum_engine.quantum_status()


@router.post("/optimize/portfolio")
def optimize_portfolio(request: PortfolioRequest):
    """
    Problema 1: Optimización de portafolio (QAOA).
    Selecciona el subconjunto óptimo de activos maximizando retorno/riesgo.
    """
    return quantum_engine.optimize_portfolio(
        returns=request.returns,
        risks=request.risks,
        budget=request.budget,
        risk_aversion=request.risk_aversion,
    )


@router.post("/optimize/payments")
def optimize_payments(request: PaymentScheduleRequest):
    """
    Problema 2: Scheduling de pagos.
    Optimiza qué pagar ahora para minimizar penalizaciones respetando la caja.
    """
    payments = [p.dict() for p in request.payments]
    return quantum_engine.schedule_payments(payments, request.available_cash)


@router.post("/optimize/resources")
def optimize_resources(request: ResourceAllocationRequest):
    """
    Problema 3: Asignación de recursos.
    Distribuye recursos limitados entre proyectos maximizando ROI total.
    """
    projects = [p.dict() for p in request.projects]
    return quantum_engine.allocate_resources(projects, request.total_resources)

"""
O-IAxis Quantum Engine Service (backend wrapper)
Importa los optimizadores cuánticos desde el módulo quantum/ de la raíz del monorepo.

REGLA DE ORO: simulador (PennyLane) siempre en dev/testing.
Si PennyLane no está disponible, degradación elegante a heurística clásica
(Protocolo de Contingencia Cuántica, Doc1 sección 1.5).
"""

import os
import sys
from typing import List, Dict

# Añadir la raíz del monorepo al path para importar quantum/
_MONOREPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _MONOREPO_ROOT not in sys.path:
    sys.path.insert(0, _MONOREPO_ROOT)

QUANTUM_AVAILABLE = True
try:
    from quantum.algorithms.quantum_optimizer import (
        get_portfolio_optimizer,
        get_payment_scheduler,
        get_resource_allocator,
    )
except Exception:
    QUANTUM_AVAILABLE = False


# ============================================================
# DEGRADACIÓN ELEGANTE - Heurísticas clásicas de respaldo
# ============================================================

def _classical_portfolio(returns, risks, budget, risk_aversion):
    """Fallback clásico para optimización de portafolio (greedy por score)."""
    scores = [(r - risk_aversion * k, i) for i, (r, k) in enumerate(zip(returns, risks))]
    scores.sort(reverse=True)
    selected = sorted([i for _, i in scores[:budget]])
    return {
        "algorithm": "Classical Greedy (quantum fallback)",
        "device": "classical-cpu",
        "selected_assets": selected,
        "expected_return": round(sum(returns[i] for i in selected), 4),
        "total_risk": round(sum(risks[i] for i in selected), 4),
        "degraded_mode": True,
    }


def _classical_payments(payments, available_cash):
    """Fallback clásico para scheduling de pagos (greedy por penalización/monto)."""
    ranked = sorted(
        range(len(payments)),
        key=lambda i: payments[i].get("penalizacion", 0) / (payments[i].get("monto", 1) + 1),
        reverse=True,
    )
    pay_now, cash = [], 0.0
    for i in ranked:
        m = payments[i].get("monto", 0)
        if cash + m <= available_cash:
            pay_now.append(i)
            cash += m
    return {
        "algorithm": "Classical Greedy (quantum fallback)",
        "device": "classical-cpu",
        "pay_immediately": sorted(pay_now),
        "defer_payment": sorted(set(range(len(payments))) - set(pay_now)),
        "cash_required": round(cash, 2),
        "degraded_mode": True,
    }


def _classical_allocation(projects, total_resources):
    """Fallback clásico para asignación de recursos (greedy por ROI/costo)."""
    ranked = sorted(
        range(len(projects)),
        key=lambda i: projects[i].get("roi", 0) / (projects[i].get("costo", 1) + 1),
        reverse=True,
    )
    funded, cost = [], 0.0
    for i in ranked:
        c = projects[i].get("costo", 0)
        if cost + c <= total_resources:
            funded.append(i)
            cost += c
    return {
        "algorithm": "Classical Greedy (quantum fallback)",
        "device": "classical-cpu",
        "funded_projects": [
            {"index": i, "nombre": projects[i].get("nombre", f"Proyecto {i}")} for i in funded
        ],
        "total_cost": round(cost, 2),
        "degraded_mode": True,
    }


# ============================================================
# API PÚBLICA DEL SERVICIO
# ============================================================

def optimize_portfolio(returns, risks, budget, risk_aversion=0.5) -> Dict:
    if QUANTUM_AVAILABLE:
        return get_portfolio_optimizer().optimize(returns, risks, budget, risk_aversion)
    return _classical_portfolio(returns, risks, budget, risk_aversion)


def schedule_payments(payments, available_cash) -> Dict:
    if QUANTUM_AVAILABLE:
        return get_payment_scheduler().optimize_schedule(payments, available_cash)
    return _classical_payments(payments, available_cash)


def allocate_resources(projects, total_resources) -> Dict:
    if QUANTUM_AVAILABLE:
        return get_resource_allocator().allocate(projects, total_resources)
    return _classical_allocation(projects, total_resources)


def quantum_status() -> Dict:
    return {
        "quantum_available": QUANTUM_AVAILABLE,
        "backend": "PennyLane default.qubit (simulator)" if QUANTUM_AVAILABLE else "classical fallback",
        "rule": "QPU real solo en lote semanal de producción (domingo)",
    }

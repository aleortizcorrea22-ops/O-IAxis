"""
O-IAxis Quantum Optimization Engine
Computación cuántica para los 3 problemas combinatorios nativos (Doc1, sección 1.4)

REGLA DE ORO (Doc2, sección 1.3):
En desarrollo y testing usar SIEMPRE PennyLane o Qiskit-Aer (simuladores).
Nunca gastar créditos de QPU real en código no validado.
Los créditos IBM Quantum se usan solo en el lote semanal de producción del domingo.
"""

from typing import List, Dict, Tuple, Optional
import pennylane as qml
from pennylane import numpy as pnp
import numpy as np


# ============================================================
# CONFIGURACIÓN DEL DISPOSITIVO CUÁNTICO
# ============================================================

class QuantumDevice:
    """
    Gestor del dispositivo cuántico con degradación elegante.
    Protocolo de Contingencia Cuántica (Doc1, sección 1.5).
    """

    def __init__(self, mode: str = "simulator"):
        """
        mode: 'simulator' (default, dev/testing) | 'qpu' (solo producción domingo)
        """
        self.mode = mode
        self.backend = "default.qubit"  # Simulador PennyLane

    def get_device(self, wires: int):
        """Obtener dispositivo cuántico. Siempre simulador salvo orden explícita."""
        if self.mode == "qpu":
            # En producción real conectaría a IBM Quantum.
            # Por seguridad, en este entorno usamos siempre el simulador.
            pass
        return qml.device(self.backend, wires=wires)


# ============================================================
# PROBLEMA 1: OPTIMIZACIÓN DE PORTAFOLIO (QAOA)
# ============================================================

class PortfolioOptimizer:
    """
    Optimización de portafolio de inversiones usando QAOA.
    Selecciona el subconjunto óptimo de activos maximizando retorno/riesgo.
    """

    def __init__(self, device_mode: str = "simulator"):
        self.qdevice = QuantumDevice(device_mode)

    def optimize(
        self,
        returns: List[float],
        risks: List[float],
        budget: int,
        risk_aversion: float = 0.5
    ) -> Dict:
        """
        Optimiza selección de activos.

        returns: retornos esperados por activo
        risks: riesgo (varianza) por activo
        budget: número máximo de activos a seleccionar
        risk_aversion: factor de aversión al riesgo (0-1)
        """
        n_assets = len(returns)
        if n_assets == 0:
            return {"error": "No assets provided"}

        # Limitar a tamaño manejable para simulación
        n_qubits = min(n_assets, 8)

        returns_arr = np.array(returns[:n_qubits])
        risks_arr = np.array(risks[:n_qubits])

        # Normalizar
        if returns_arr.max() > 0:
            returns_norm = returns_arr / returns_arr.max()
        else:
            returns_norm = returns_arr
        if risks_arr.max() > 0:
            risks_norm = risks_arr / risks_arr.max()
        else:
            risks_norm = risks_arr

        # Score combinado: retorno - aversión*riesgo
        scores = returns_norm - risk_aversion * risks_norm

        dev = self.qdevice.get_device(n_qubits)

        @qml.qnode(dev)
        def circuit(params):
            # Estado inicial superpuesto
            for i in range(n_qubits):
                qml.Hadamard(wires=i)
            # Capa parametrizada (ansatz QAOA simplificado)
            for i in range(n_qubits):
                qml.RY(params[i], wires=i)
            for i in range(n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
            # Medir expectativa ponderada por scores
            return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

        # Optimización clásica de parámetros
        params = pnp.array(np.random.uniform(0, np.pi, n_qubits), requires_grad=True)
        opt = qml.GradientDescentOptimizer(stepsize=0.3)

        def cost(params):
            expvals = circuit(params)
            # Queremos seleccionar activos con score alto
            selection = [(1 - e) / 2 for e in expvals]
            total = sum(s * sc for s, sc in zip(selection, scores))
            penalty = abs(sum(selection) - budget) * 0.5
            return -total + penalty

        for _ in range(30):
            params = opt.step(cost, params)

        # Resultado final
        final_expvals = circuit(params)
        selection_probs = [(1 - float(e)) / 2 for e in final_expvals]

        # Seleccionar top-budget activos
        ranked = sorted(
            range(n_qubits),
            key=lambda i: selection_probs[i],
            reverse=True
        )
        selected = sorted(ranked[:budget])

        expected_return = sum(returns[i] for i in selected)
        total_risk = sum(risks[i] for i in selected)

        return {
            "algorithm": "QAOA Portfolio Optimization",
            "device": "simulator (PennyLane default.qubit)",
            "selected_assets": selected,
            "selection_probabilities": [round(p, 4) for p in selection_probs],
            "expected_return": round(expected_return, 4),
            "total_risk": round(total_risk, 4),
            "sharpe_estimate": round(expected_return / (total_risk + 1e-6), 4),
            "n_qubits_used": n_qubits
        }


# ============================================================
# PROBLEMA 2: SCHEDULING DE PAGOS (Combinatorial)
# ============================================================

class PaymentScheduler:
    """
    Optimización del calendario de pagos para maximizar liquidez
    minimizando penalizaciones por mora.
    """

    def __init__(self, device_mode: str = "simulator"):
        self.qdevice = QuantumDevice(device_mode)

    def optimize_schedule(
        self,
        payments: List[Dict],
        available_cash: float
    ) -> Dict:
        """
        payments: lista de {'monto': float, 'penalizacion': float, 'prioridad': int}
        available_cash: efectivo disponible
        """
        n_payments = len(payments)
        if n_payments == 0:
            return {"error": "No payments to schedule"}

        n_qubits = min(n_payments, 8)
        payments_subset = payments[:n_qubits]

        montos = np.array([p.get("monto", 0) for p in payments_subset])
        penalizaciones = np.array([p.get("penalizacion", 0) for p in payments_subset])

        dev = self.qdevice.get_device(n_qubits)

        @qml.qnode(dev)
        def circuit(params):
            for i in range(n_qubits):
                qml.Hadamard(wires=i)
            for i in range(n_qubits):
                qml.RY(params[i], wires=i)
            for i in range(n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
            return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

        params = pnp.array(np.random.uniform(0, np.pi, n_qubits), requires_grad=True)
        opt = qml.GradientDescentOptimizer(stepsize=0.3)

        def cost(params):
            expvals = circuit(params)
            pay_now = [(1 - e) / 2 for e in expvals]
            # Minimizar penalizaciones no pagadas, respetar cash
            saved_penalties = sum(p * pen for p, pen in zip(pay_now, penalizaciones))
            cash_used = sum(p * m for p, m in zip(pay_now, montos))
            penalty = max(0, cash_used - available_cash) * 0.1
            return -saved_penalties + penalty

        for _ in range(30):
            params = opt.step(cost, params)

        final_expvals = circuit(params)
        pay_decision = [(1 - float(e)) / 2 > 0.5 for e in final_expvals]

        scheduled_now = [i for i, d in enumerate(pay_decision) if d]
        deferred = [i for i, d in enumerate(pay_decision) if not d]

        cash_required = sum(montos[i] for i in scheduled_now)
        penalties_avoided = sum(penalizaciones[i] for i in scheduled_now)

        return {
            "algorithm": "Quantum Payment Scheduling",
            "device": "simulator (PennyLane default.qubit)",
            "pay_immediately": scheduled_now,
            "defer_payment": deferred,
            "cash_required": round(float(cash_required), 2),
            "cash_available": round(available_cash, 2),
            "penalties_avoided": round(float(penalties_avoided), 2),
            "feasible": bool(cash_required <= available_cash)
        }


# ============================================================
# PROBLEMA 3: ASIGNACIÓN DE RECURSOS (Resource Allocation)
# ============================================================

class ResourceAllocator:
    """
    Asignación óptima de recursos limitados entre proyectos/áreas
    maximizando el retorno total esperado.
    """

    def __init__(self, device_mode: str = "simulator"):
        self.qdevice = QuantumDevice(device_mode)

    def allocate(
        self,
        projects: List[Dict],
        total_resources: float
    ) -> Dict:
        """
        projects: lista de {'roi': float, 'costo': float, 'nombre': str}
        total_resources: recursos totales disponibles
        """
        n_projects = len(projects)
        if n_projects == 0:
            return {"error": "No projects provided"}

        n_qubits = min(n_projects, 8)
        proj_subset = projects[:n_qubits]

        rois = np.array([p.get("roi", 0) for p in proj_subset])
        costos = np.array([p.get("costo", 0) for p in proj_subset])

        dev = self.qdevice.get_device(n_qubits)

        @qml.qnode(dev)
        def circuit(params):
            for i in range(n_qubits):
                qml.Hadamard(wires=i)
            for layer in range(2):
                for i in range(n_qubits):
                    qml.RY(params[layer * n_qubits + i], wires=i)
                for i in range(n_qubits - 1):
                    qml.CNOT(wires=[i, i + 1])
            return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

        params = pnp.array(np.random.uniform(0, np.pi, 2 * n_qubits), requires_grad=True)
        opt = qml.GradientDescentOptimizer(stepsize=0.3)

        def cost(params):
            expvals = circuit(params)
            fund = [(1 - e) / 2 for e in expvals]
            total_roi = sum(f * r for f, r in zip(fund, rois))
            cost_used = sum(f * c for f, c in zip(fund, costos))
            penalty = max(0, cost_used - total_resources) * 0.1
            return -total_roi + penalty

        for _ in range(40):
            params = opt.step(cost, params)

        final_expvals = circuit(params)
        fund_decision = [(1 - float(e)) / 2 > 0.5 for e in final_expvals]

        funded = [i for i, d in enumerate(fund_decision) if d]

        total_cost = sum(costos[i] for i in funded)
        total_roi = sum(rois[i] for i in funded)

        return {
            "algorithm": "Quantum Resource Allocation",
            "device": "simulator (PennyLane default.qubit)",
            "funded_projects": [
                {"index": i, "nombre": proj_subset[i].get("nombre", f"Proyecto {i}")}
                for i in funded
            ],
            "total_cost": round(float(total_cost), 2),
            "total_resources": round(total_resources, 2),
            "expected_total_roi": round(float(total_roi), 4),
            "resources_remaining": round(total_resources - float(total_cost), 2),
            "feasible": bool(total_cost <= total_resources)
        }


# ============================================================
# FACTORY
# ============================================================

def get_portfolio_optimizer() -> PortfolioOptimizer:
    return PortfolioOptimizer()


def get_payment_scheduler() -> PaymentScheduler:
    return PaymentScheduler()


def get_resource_allocator() -> ResourceAllocator:
    return ResourceAllocator()

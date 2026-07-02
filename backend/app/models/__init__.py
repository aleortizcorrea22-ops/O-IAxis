"""
Import all models for database creation
"""

from app.models.base import BaseModel

# M2 - Tesorería
from app.models.m2_tesoreria import (
    TesoreriaTransaction, CajaDiaria, FlujoCaja,
    TransactionType, TransactionStatus
)

# M5 - Fiscal
from app.models.m5_fiscal import (
    ImpuestoDetalle, FiscalObligacion, RetencionesCobradas, ResultadoFiscalProyectado,
    TaxType, FiscalObligationType
)

# M1 - Control Operativo
from app.models.m1_control_operativo import (
    IndicadorOperacional, Proceso, RegistroAuditoria, MetricaDesempenio,
    AreaOperativa
)

# M3 - Flujos Internos
from app.models.m3_flujos_internos import (
    FlujoInterno, RotacionFondos, AsignacionPresupuestaria, ProjectionFlujoCaja,
    TipoFlujoInterno
)

# M4 - Contexto Macroeconómico
from app.models.m4_macro import (
    IndicadorMacroeconomico, ImpactoMacroEmpresa, EscenarioMacro, SensibilidadMacro,
    VariableMacro
)

# M6 - Patrimonio
from app.models.m6_patrimonio import (
    Activo, Pasivo, EstadoPatrimonial, RatiosCapital
)

# M7-M12 - Finanzas de Frontera
from app.models.m7_m12_frontera import (
    CreditScore, CapitalTrabajo, PricingIntelligence,
    InversionAvanzada, AlertaFraude, BenchmarkSectorial
)

__all__ = [
    # Base
    "BaseModel",
    # M2
    "TesoreriaTransaction", "CajaDiaria", "FlujoCaja",
    "TransactionType", "TransactionStatus",
    # M5
    "ImpuestoDetalle", "FiscalObligacion", "RetencionesCobradas", "ResultadoFiscalProyectado",
    "TaxType", "FiscalObligationType",
    # M1
    "IndicadorOperacional", "Proceso", "RegistroAuditoria", "MetricaDesempenio",
    "AreaOperativa",
    # M3
    "FlujoInterno", "RotacionFondos", "AsignacionPresupuestaria", "ProjectionFlujoCaja",
    "TipoFlujoInterno",
    # M4
    "IndicadorMacroeconomico", "ImpactoMacroEmpresa", "EscenarioMacro", "SensibilidadMacro",
    "VariableMacro",
    # M6
    "Activo", "Pasivo", "EstadoPatrimonial", "RatiosCapital",
    # M7-M12
    "CreditScore", "CapitalTrabajo", "PricingIntelligence",
    "InversionAvanzada", "AlertaFraude", "BenchmarkSectorial",
]

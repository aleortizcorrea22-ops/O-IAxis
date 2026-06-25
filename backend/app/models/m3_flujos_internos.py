"""
M3 Flujos de Efectivo Internos (Internal Cash Flows Management)
Motor 3: Gestión de flujos internos de caja y fondos
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, Enum, ForeignKey
from datetime import date
import enum
from app.models.base import BaseModel


class TipoFlujoInterno(str, enum.Enum):
    """Tipos de flujos internos"""
    PAGO_NOMINA = "pago_nomina"
    PAGO_PROVEEDORES = "pago_proveedores"
    COBROS_CLIENTES = "cobros_clientes"
    DIVIDENDOS = "dividendos"
    INVERSION_CAPITAL = "inversion_capital"
    PRESTAMOS = "prestamos"
    COBRO_PRESTAMOS = "cobro_prestamos"
    GASTOS_OPERATIVOS = "gastos_operativos"


class FlujoInterno(BaseModel):
    """Registro de flujo interno"""

    __tablename__ = "m3_flujo_interno"

    empresa_id = Column(Integer, nullable=False, index=True)
    tipo_flujo = Column(Enum(TipoFlujoInterno), nullable=False, index=True)
    fecha_programada = Column(Date, nullable=False, index=True)
    fecha_ejecutado = Column(Date, nullable=True)
    monto = Column(Float, nullable=False)
    centro_costo = Column(String(100), nullable=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(20), default="programado")  # programado, ejecutado, cancelado
    referencia = Column(String(100), unique=True, nullable=False)


class RotacionFondos(BaseModel):
    """Ciclo de rotación de fondos"""

    __tablename__ = "m3_rotacion_fondos"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    dias_rotacion = Column(Float, nullable=False)
    monto_rotado = Column(Float, nullable=False)
    eficiencia = Column(Float, nullable=False)  # porcentaje
    velocidad_circulante = Column(Float, nullable=True)
    descripcion = Column(Text, nullable=True)


class AsignacionPresupuestaria(BaseModel):
    """Asignación de presupuesto por centro de costo"""

    __tablename__ = "m3_asignacion_presupuestaria"

    empresa_id = Column(Integer, nullable=False, index=True)
    centro_costo = Column(String(100), nullable=False, index=True)
    periodo = Column(String(20), nullable=False)  # YYYY-MM
    presupuesto_asignado = Column(Float, nullable=False)
    gasto_ejecutado = Column(Float, default=0.0)
    disponibilidad = Column(Float, nullable=False)
    porcentaje_ejecucion = Column(Float, nullable=False)
    responsable = Column(String(200), nullable=True)
    observaciones = Column(Text, nullable=True)


class ProjectionFlujoCaja(BaseModel):
    """Proyección detallada de flujo de caja"""

    __tablename__ = "m3_proyeccion_flujo"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha_inicio = Column(Date, nullable=False, index=True)
    fecha_fin = Column(Date, nullable=False)
    escenario = Column(String(20), nullable=False)  # base, optimista, pesimista
    saldo_inicial = Column(Float, nullable=False)
    ingresos_proyectados = Column(Float, nullable=False)
    egresos_proyectados = Column(Float, nullable=False)
    saldo_final_proyectado = Column(Float, nullable=False)
    confianza = Column(Float, nullable=False)  # 0-1
    metodologia = Column(String(100), nullable=True)

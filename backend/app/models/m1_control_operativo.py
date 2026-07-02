"""
M1 Control Operativo Interno (Internal Operational Control)
Motor 1: GestiÃ³n y control de operaciones internas
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, Enum, Boolean, JSON
from datetime import date
import enum
from app.models.base import BaseModel


class AreaOperativa(str, enum.Enum):
    """Ãreas operativas de la empresa"""
    VENTAS = "ventas"
    COMPRAS = "compras"
    PRODUCCION = "produccion"
    RRHH = "rrhh"
    ADMINISTRACION = "administracion"
    LOGISTICA = "logistica"


class IndicadorOperacional(BaseModel):
    """Indicadores operacionales clave"""

    __tablename__ = "m1_indicador_operacional"

    empresa_id = Column(Integer, nullable=False, index=True)
    area = Column(String(50), nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    nombre_indicador = Column(String(200), nullable=False)
    valor_actual = Column(Float, nullable=False)
    valor_target = Column(Float, nullable=True)
    variacion_porcentaje = Column(Float, nullable=False)
    estado = Column(String(20), default="normal")  # normal, alerta, critico
    descripcion = Column(Text, nullable=True)


class Proceso(BaseModel):
    """Procesos operacionales definidos"""

    __tablename__ = "m1_proceso"

    empresa_id = Column(Integer, nullable=False, index=True)
    codigo_proceso = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    area = Column(String(50), nullable=False)
    responsable = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    periodicidad = Column(String(50), nullable=True)  # diaria, semanal, mensual
    activo = Column(Boolean, default=True)


class RegistroAuditoria(BaseModel):
    """Registro de auditorÃ­a de procesos"""

    __tablename__ = "m1_registro_auditoria"

    empresa_id = Column(Integer, nullable=False, index=True)
    proceso_id = Column(Integer, nullable=False, index=True)
    fecha_ejecucion = Column(Date, nullable=False, index=True)
    cumplimiento_porcentaje = Column(Float, nullable=False)
    observaciones = Column(Text, nullable=True)
    hallazgos_criticos = Column(Integer, default=0)
    hallazgos_mayores = Column(Integer, default=0)
    hallazgos_menores = Column(Integer, default=0)
    estado = Column(String(20), default="completado")


class MetricaDesempenio(BaseModel):
    """MÃ©tricas de desempeÃ±o operacional"""

    __tablename__ = "m1_metrica_desempenio"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    eficiencia_operativa = Column(Float, nullable=False)  # 0-100
    calidad_procesos = Column(Float, nullable=False)
    cumplimiento_sla = Column(Float, nullable=False)
    satisfaccion_cliente = Column(Float, nullable=True)
    productividad = Column(Float, nullable=False)
    tendencia = Column(String(20), nullable=True)  # mejorando, estable, deterioro

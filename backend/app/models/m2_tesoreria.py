"""
M2 Tesorería (Treasury/Cash Management) Engine Models
Motor 2: Gestión de Tesorería y Flujos de Efectivo
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
import enum
from app.models.base import BaseModel


class TransactionType(str, enum.Enum):
    """Tipos de transacciones de tesorería"""
    INGRESOS = "ingresos"
    EGRESOS = "egresos"
    TRANSFERENCIAS = "transferencias"
    INVERSIONES = "inversiones"


class TransactionStatus(str, enum.Enum):
    """Estado de las transacciones"""
    PROGRAMADA = "programada"
    PENDIENTE = "pendiente"
    EJECUTADA = "ejecutada"
    CANCELADA = "cancelada"


class TesoreriaTransaction(BaseModel):
    """Transacción de tesorería individual"""

    __tablename__ = "m2_transactions"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha_transaccion = Column(Date, nullable=False, index=True)
    tipo = Column(Enum(TransactionType), nullable=False)
    monto = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=True)
    referencia = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDIENTE)
    cuenta_origen = Column(String(50), nullable=True)
    cuenta_destino = Column(String(50), nullable=True)
    moneda = Column(String(3), default="ARS", nullable=False)


class CajaDiaria(BaseModel):
    """Posición de caja diaria"""

    __tablename__ = "m2_caja_diaria"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, unique=True, index=True)
    saldo_inicial = Column(Float, default=0.0)
    ingresos = Column(Float, default=0.0)
    egresos = Column(Float, default=0.0)
    saldo_final = Column(Float, default=0.0)
    moneda = Column(String(3), default="ARS")


class FlujoCaja(BaseModel):
    """Proyección de flujo de caja"""

    __tablename__ = "m2_flujo_caja"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    periodicidad = Column(String(20), nullable=False)  # diaria, semanal, mensual
    saldo_proyectado = Column(Float, nullable=False)
    confianza = Column(Float, nullable=False)  # 0-1 (0%-100%)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(20), default="activo")

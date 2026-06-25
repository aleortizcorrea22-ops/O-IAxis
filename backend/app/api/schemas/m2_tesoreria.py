"""
Pydantic schemas for M2 Tesorería (Treasury) API
"""

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class TransactionTypeEnum(str, Enum):
    INGRESOS = "ingresos"
    EGRESOS = "egresos"
    TRANSFERENCIAS = "transferencias"
    INVERSIONES = "inversiones"


class TransactionStatusEnum(str, Enum):
    PROGRAMADA = "programada"
    PENDIENTE = "pendiente"
    EJECUTADA = "ejecutada"
    CANCELADA = "cancelada"


class TesoreriaTransactionCreate(BaseModel):
    """Schema para crear una transacción"""
    empresa_id: int
    fecha_transaccion: date
    tipo: TransactionTypeEnum
    monto: float = Field(gt=0)
    descripcion: Optional[str] = None
    referencia: str
    cuenta_origen: Optional[str] = None
    cuenta_destino: Optional[str] = None
    moneda: str = "ARS"


class TesoreriaTransactionResponse(BaseModel):
    """Schema para responder con una transacción"""
    id: int
    empresa_id: int
    fecha_transaccion: date
    tipo: TransactionTypeEnum
    monto: float
    descripcion: Optional[str]
    referencia: str
    status: TransactionStatusEnum
    cuenta_origen: Optional[str]
    cuenta_destino: Optional[str]
    moneda: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CajaDiariaCreate(BaseModel):
    """Schema para crear registro de caja diaria"""
    empresa_id: int
    fecha: date
    saldo_inicial: float
    ingresos: float
    egresos: float
    moneda: str = "ARS"


class CajaDiariaResponse(BaseModel):
    """Schema para responder con caja diaria"""
    id: int
    empresa_id: int
    fecha: date
    saldo_inicial: float
    ingresos: float
    egresos: float
    saldo_final: float
    moneda: str
    created_at: datetime

    class Config:
        from_attributes = True


class FlujoCajaCreate(BaseModel):
    """Schema para crear proyección de flujo de caja"""
    empresa_id: int
    fecha_inicio: date
    fecha_fin: date
    periodicidad: str  # diaria, semanal, mensual
    saldo_proyectado: float
    confianza: float = Field(ge=0, le=1)
    descripcion: Optional[str] = None


class FlujoCajaResponse(BaseModel):
    """Schema para responder con flujo de caja"""
    id: int
    empresa_id: int
    fecha_inicio: date
    fecha_fin: date
    periodicidad: str
    saldo_proyectado: float
    confianza: float
    descripcion: Optional[str]
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True


class TesoreriaResumenResponse(BaseModel):
    """Resumen de posición de tesorería"""
    empresa_id: int
    saldo_actual: float
    ingresos_mes: float
    egresos_mes: float
    flujo_neto: float
    proyeccion_flujo: List[FlujoCajaResponse]
    transacciones_pendientes: int
    fecha_actualizacion: datetime

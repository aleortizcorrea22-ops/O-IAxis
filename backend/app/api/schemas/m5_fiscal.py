"""
Pydantic schemas for M5 Fiscal (Tax Management) API
"""

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class TaxTypeEnum(str, Enum):
    IVA = "iva"
    INGRESOS_BRUTOS = "ingresos_brutos"
    GANANCIAS = "ganancias"
    APORTACIONES = "aportaciones"
    AFIP = "afip"


class FiscalObligationTypeEnum(str, Enum):
    DECLARACION = "declaracion"
    PAGO = "pago"
    RETENCION = "retencion"
    PERCEPCION = "percepcion"
    INSCRIPCION = "inscripcion"


class ImpuestoDetalleCreate(BaseModel):
    """Schema para crear detalle de impuesto"""
    empresa_id: int
    tipo_impuesto: TaxTypeEnum
    periodo: str  # YYYYMM
    fecha_vencimiento: date
    base_imponible: float = Field(ge=0)
    alicuota: float = Field(ge=0, le=100)
    monto_impuesto: float = Field(ge=0)
    descripcion: Optional[str] = None


class ImpuestoDetalleResponse(BaseModel):
    """Schema para responder con detalle de impuesto"""
    id: int
    empresa_id: int
    tipo_impuesto: TaxTypeEnum
    periodo: str
    fecha_vencimiento: date
    base_imponible: float
    alicuota: float
    monto_impuesto: float
    monto_pagado: float
    descripcion: Optional[str]
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True


class FiscalObligacionCreate(BaseModel):
    """Schema para crear obligación fiscal"""
    empresa_id: int
    tipo: FiscalObligationTypeEnum
    descripcion: str
    fecha_vencimiento: date
    url_formulario: Optional[str] = None


class FiscalObligacionResponse(BaseModel):
    """Schema para responder con obligación fiscal"""
    id: int
    empresa_id: int
    tipo: FiscalObligationTypeEnum
    descripcion: str
    fecha_vencimiento: date
    estatus: str
    url_formulario: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RetencionesCobradas​Create(BaseModel):
    """Schema para registrar retenciones cobradas"""
    empresa_id: int
    fecha: date
    numero_comprobante: str
    razon_social_tercero: str
    cuit_tercero: str
    tipo_impuesto: TaxTypeEnum
    monto_retenido: float = Field(gt=0)
    descripcion: Optional[str] = None


class RetencionesCobradas​Response(BaseModel):
    """Schema para responder con retenciones cobradas"""
    id: int
    empresa_id: int
    fecha: date
    numero_comprobante: str
    razon_social_tercero: str
    cuit_tercero: str
    tipo_impuesto: TaxTypeEnum
    monto_retenido: float
    descripcion: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ResultadoFiscalProyectadoCreate(BaseModel):
    """Schema para crear proyección de resultado fiscal"""
    empresa_id: int
    periodo: str  # YYYY o YYYYMM
    ingresos_proyectados: float = Field(ge=0)
    gastos_proyectados: float = Field(ge=0)
    impuestos_estimados: float = Field(ge=0)
    confianza: float = Field(ge=0, le=1)
    notas: Optional[str] = None


class ResultadoFiscalProyectadoResponse(BaseModel):
    """Schema para responder con proyección de resultado fiscal"""
    id: int
    empresa_id: int
    periodo: str
    ingresos_proyectados: float
    gastos_proyectados: float
    impuestos_estimados: float
    resultado_neto: float
    tasa_efectiva_impositiva: float
    confianza: float
    notas: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class FiscalResumenResponse(BaseModel):
    """Resumen de posición fiscal"""
    empresa_id: int
    impuestos_pendientes: List[ImpuestoDetalleResponse]
    obligaciones_proximas: List[FiscalObligacionResponse]
    monto_total_adeudado: float
    monto_retenciones_acumulado: float
    proyeccion_anual: Optional[ResultadoFiscalProyectadoResponse]
    fecha_actualizacion: datetime

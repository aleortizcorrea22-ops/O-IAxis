"""
M5 Fiscal (Tax Management) Engine Models
Motor 5: Gestión Fiscal e Impositiva
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, Enum, Boolean
from datetime import date
import enum
from app.models.base import BaseModel


class TaxType(str, enum.Enum):
    """Tipos de impuestos"""
    IVA = "iva"
    INGRESOS_BRUTOS = "ingresos_brutos"
    GANANCIAS = "ganancias"
    APORTACIONES = "aportaciones"
    AFIP = "afip"


class FiscalObligationType(str, enum.Enum):
    """Tipos de obligaciones fiscales"""
    DECLARACION = "declaracion"
    PAGO = "pago"
    RETENCION = "retencion"
    PERCEPCION = "percepcion"
    INSCRIPCION = "inscripcion"


class ImpuestoDetalle(BaseModel):
    """Detalle de impuesto individual"""

    __tablename__ = "m5_impuesto_detalle"

    empresa_id = Column(Integer, nullable=False, index=True)
    tipo_impuesto = Column(Enum(TaxType), nullable=False)
    periodo = Column(String(20), nullable=False)  # YYYYMM format
    fecha_vencimiento = Column(Date, nullable=False, index=True)
    base_imponible = Column(Float, nullable=False)
    alicuota = Column(Float, nullable=False)  # porcentaje
    monto_impuesto = Column(Float, nullable=False)
    monto_pagado = Column(Float, default=0.0)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(20), default="pendiente")  # pendiente, pagado, vencido


class FiscalObligacion(BaseModel):
    """Obligación fiscal importante"""

    __tablename__ = "m5_obligacion"

    empresa_id = Column(Integer, nullable=False, index=True)
    tipo = Column(Enum(FiscalObligationType), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False, index=True)
    estatus = Column(String(20), default="pendiente")
    url_formulario = Column(String(500), nullable=True)


class RetencionesCobradas(BaseModel):
    """Registro de retenciones cobradas a terceros"""

    __tablename__ = "m5_retenciones_cobradas"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False)
    numero_comprobante = Column(String(50), unique=True, nullable=False)
    razon_social_tercero = Column(String(200), nullable=False)
    cuit_tercero = Column(String(13), nullable=False)
    tipo_impuesto = Column(Enum(TaxType), nullable=False)
    monto_retenido = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=True)


class ResultadoFiscalProyectado(BaseModel):
    """Proyección de resultado fiscal"""

    __tablename__ = "m5_resultado_proyectado"

    empresa_id = Column(Integer, nullable=False, index=True)
    periodo = Column(String(20), nullable=False, unique=True)  # YYYY o YYYYMM
    ingresos_proyectados = Column(Float, nullable=False)
    gastos_proyectados = Column(Float, nullable=False)
    impuestos_estimados = Column(Float, nullable=False)
    resultado_neto = Column(Float, nullable=False)
    tasa_efectiva_impositiva = Column(Float, nullable=False)  # porcentaje
    confianza = Column(Float, nullable=False)  # 0-1
    notas = Column(Text, nullable=True)

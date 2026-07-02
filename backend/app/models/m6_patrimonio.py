"""
M6 Patrimonio y Estructura de Capital (Net Worth & Capital Structure)
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, Boolean
from app.models.base import BaseModel


class Activo(BaseModel):
    """Registro de activos"""

    __tablename__ = "m6_activo"

    empresa_id = Column(Integer, nullable=False, index=True)
    tipo_activo = Column(String(50), nullable=False, index=True)
    descripcion = Column(String(200), nullable=False)
    valor_libro = Column(Float, nullable=False)
    valor_mercado = Column(Float, nullable=True)
    fecha_adquisicion = Column(Date, nullable=True)
    vida_util_anos = Column(Integer, nullable=True)
    depreciacion_acumulada = Column(Float, default=0.0)
    activo = Column(Boolean, default=True)
    ubicacion = Column(String(200), nullable=True)
    observaciones = Column(Text, nullable=True)


class Pasivo(BaseModel):
    """Registro de pasivos"""

    __tablename__ = "m6_pasivo"

    empresa_id = Column(Integer, nullable=False, index=True)
    tipo_pasivo = Column(String(50), nullable=False, index=True)
    descripcion = Column(String(200), nullable=False)
    monto_total = Column(Float, nullable=False)
    monto_pagado = Column(Float, default=0.0)
    fecha_vencimiento = Column(Date, nullable=True)
    tasa_interes = Column(Float, nullable=True)
    plazo_meses = Column(Integer, nullable=True)
    acreedor = Column(String(200), nullable=True)
    condiciones = Column(Text, nullable=True)


class EstadoPatrimonial(BaseModel):
    """Estado patrimonial (Balance Sheet)"""

    __tablename__ = "m6_estado_patrimonial"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True, unique=True)
    total_activos = Column(Float, nullable=False)
    total_pasivos = Column(Float, nullable=False)
    patrimonio = Column(Float, nullable=False)
    pasivos_corrientes = Column(Float, nullable=False)
    pasivos_no_corrientes = Column(Float, nullable=False)
    activos_corrientes = Column(Float, nullable=False)
    activos_no_corrientes = Column(Float, nullable=False)


class RatiosCapital(BaseModel):
    """Ratios de estructura de capital"""

    __tablename__ = "m6_ratios_capital"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    ratio_deuda_patrimonio = Column(Float, nullable=False)
    ratio_deuda_activos = Column(Float, nullable=False)
    ratio_solvencia = Column(Float, nullable=False)
    cobertura_interes = Column(Float, nullable=True)
    apalancamiento_financiero = Column(Float, nullable=False)
    capital_trabajo = Column(Float, nullable=False)
    liquidez_general = Column(Float, nullable=False)
    liquidez_inmediata = Column(Float, nullable=False)
    tendencia = Column(String(20), nullable=True)

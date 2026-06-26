"""
Motores M7-M12 — Eje C: Finanzas de Frontera e Inteligencia Distribuida
(Doc1, sección 2.4)

M7  - Inteligencia de Crédito y Scoring Alternativo
M8  - Optimización de Capital de Trabajo
M9  - Inteligencia de Mercado y Pricing
M10 - Gestión de Inversiones y Tesorería Avanzada
M11 - Detección de Fraude y Anomalías Financieras
M12 - Inteligencia Distribuida de Red (Benchmarking Sectorial)
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, Enum, Boolean
import enum
from app.models.base import BaseModel


# ============= M7 - CRÉDITO Y SCORING =============

class CreditScore(BaseModel):
    """M7: Score crediticio con datos alternativos"""

    __tablename__ = "m7_credit_score"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    score = Column(Float, nullable=False)  # 0-1000
    rating = Column(String(5), nullable=False)  # AAA, AA, A, BBB, etc
    probabilidad_default = Column(Float, nullable=False)  # 0-1
    capacidad_pago = Column(Float, nullable=True)
    fuentes_alternativas = Column(Text, nullable=True)  # comportamiento de pago, redes, etc
    dictamen = Column(Text, nullable=True)  # carácter informativo (Doc1)


# ============= M8 - CAPITAL DE TRABAJO =============

class CapitalTrabajo(BaseModel):
    """M8: Optimización de capital de trabajo"""

    __tablename__ = "m8_capital_trabajo"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    dias_inventario = Column(Float, nullable=True)
    dias_cobro = Column(Float, nullable=True)  # DSO
    dias_pago = Column(Float, nullable=True)  # DPO
    ciclo_conversion_efectivo = Column(Float, nullable=False)  # CCC
    capital_trabajo_neto = Column(Float, nullable=False)
    recomendacion = Column(Text, nullable=True)


# ============= M9 - MERCADO Y PRICING =============

class PricingIntelligence(BaseModel):
    """M9: Inteligencia de pricing y mercado"""

    __tablename__ = "m9_pricing"

    empresa_id = Column(Integer, nullable=False, index=True)
    producto = Column(String(200), nullable=False)
    fecha = Column(Date, nullable=False, index=True)
    precio_actual = Column(Float, nullable=False)
    precio_optimo_sugerido = Column(Float, nullable=True)
    elasticidad_precio = Column(Float, nullable=True)
    margen_actual = Column(Float, nullable=True)
    posicion_competitiva = Column(String(20), nullable=True)  # premium, paridad, descuento
    dictamen = Column(Text, nullable=True)  # carácter informativo


# ============= M10 - INVERSIONES =============

class InversionAvanzada(BaseModel):
    """M10: Gestión de inversiones y tesorería avanzada"""

    __tablename__ = "m10_inversion"

    empresa_id = Column(Integer, nullable=False, index=True)
    instrumento = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)  # plazo_fijo, bono, fondo, etc
    monto_invertido = Column(Float, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=True)
    tasa_esperada = Column(Float, nullable=True)
    retorno_actual = Column(Float, default=0.0)
    riesgo = Column(String(20), nullable=True)  # bajo, medio, alto
    estado = Column(String(20), default="activa")


# ============= M11 - FRAUDE Y ANOMALÍAS =============

class AlertaFraude(BaseModel):
    """M11: Detección de fraude y anomalías financieras"""

    __tablename__ = "m11_alerta_fraude"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha_deteccion = Column(Date, nullable=False, index=True)
    tipo_anomalia = Column(String(100), nullable=False)
    severidad = Column(String(20), nullable=False)  # baja, media, alta, critica
    score_riesgo = Column(Float, nullable=False)  # 0-1
    transaccion_referencia = Column(String(100), nullable=True)
    monto_involucrado = Column(Float, nullable=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(20), default="abierta")  # abierta, investigando, cerrada
    falso_positivo = Column(Boolean, default=False)


# ============= M12 - INTELIGENCIA DISTRIBUIDA =============

class BenchmarkSectorial(BaseModel):
    """M12: Inteligencia distribuida de red (benchmarking anónimo)"""

    __tablename__ = "m12_benchmark_sectorial"

    empresa_id = Column(Integer, nullable=False, index=True)
    sector = Column(String(100), nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    metrica = Column(String(100), nullable=False)  # margen, liquidez, rotación, etc
    valor_empresa = Column(Float, nullable=False)
    percentil_sector = Column(Float, nullable=True)  # 0-100
    mediana_sector = Column(Float, nullable=True)
    mejor_cuartil = Column(Float, nullable=True)
    posicion = Column(String(20), nullable=True)  # lider, sobre_media, media, bajo_media
    insight = Column(Text, nullable=True)

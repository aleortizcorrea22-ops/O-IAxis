"""
M4 Contexto Macroeconómico (Macroeconomic Context)
Motor 4: Seguimiento de variables macroeconómicas e impacto
"""

from sqlalchemy import Column, Integer, String, Float, Date, Text, Enum
from datetime import date
import enum
from app.models.base import BaseModel


class VariableMacro(str, enum.Enum):
    """Variables macroeconómicas principales"""
    PIB = "pib"
    INFLACION = "inflacion"
    DESEMPLEO = "desempleo"
    TIPO_CAMBIO = "tipo_cambio"
    TASA_INTERES = "tasa_interes"
    RIESGO_PAIS = "riesgo_pais"
    VOLATILIDAD_MERCADO = "volatilidad_mercado"


class IndicadorMacroeconomico(BaseModel):
    """Indicadores macroeconómicos"""

    __tablename__ = "m4_indicador_macro"

    variable = Column(Enum(VariableMacro), nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True, unique=True)
    valor = Column(Float, nullable=False)
    variacion_mes = Column(Float, nullable=True)
    variacion_anual = Column(Float, nullable=True)
    proyeccion = Column(Float, nullable=True)
    fuente = Column(String(200), nullable=True)
    descripcion = Column(Text, nullable=True)


class ImpactoMacroEmpresa(BaseModel):
    """Análisis de impacto macro en empresa específica"""

    __tablename__ = "m4_impacto_macro_empresa"

    empresa_id = Column(Integer, nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    variable_macro = Column(Enum(VariableMacro), nullable=False)
    impacto_esperado = Column(String(20), nullable=False)  # positivo, negativo, neutral
    magnitud_impacto = Column(Float, nullable=False)  # porcentaje
    areas_afectadas = Column(String(500), nullable=True)  # lista separada por comas
    recomendaciones = Column(Text, nullable=True)
    confianza = Column(Float, nullable=False)  # 0-1


class EscenarioMacro(BaseModel):
    """Escenarios macroeconómicos definidos"""

    __tablename__ = "m4_escenario_macro"

    empresa_id = Column(Integer, nullable=False, index=True)
    nombre_escenario = Column(String(100), nullable=False)  # bull, base, bear
    fecha_proyeccion = Column(Date, nullable=False)
    horizonte_meses = Column(Integer, nullable=False)
    pib_crecimiento = Column(Float, nullable=True)
    inflacion_esperada = Column(Float, nullable=True)
    tipo_cambio_proyectado = Column(Float, nullable=True)
    tasa_interes_proyectada = Column(Float, nullable=True)
    probabilidad = Column(Float, nullable=False)  # 0-1
    descripcion = Column(Text, nullable=True)


class SensibilidadMacro(BaseModel):
    """Matriz de sensibilidad de empresa a variables macro"""

    __tablename__ = "m4_sensibilidad_macro"

    empresa_id = Column(Integer, nullable=False, index=True)
    variable_macro = Column(Enum(VariableMacro), nullable=False)
    elasticidad = Column(Float, nullable=False)  # cambio % en empresa por cambio % en variable
    rango_valido_min = Column(Float, nullable=True)
    rango_valido_max = Column(Float, nullable=True)
    punto_quiebre = Column(Float, nullable=True)  # valor de variable que causa crisis
    acciones_mitigacion = Column(Text, nullable=True)
    ultima_actualizacion = Column(Date, nullable=False)

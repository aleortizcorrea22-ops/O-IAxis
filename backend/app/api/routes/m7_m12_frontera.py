"""
API routes for M7-M12 — Eje C: Finanzas de Frontera (Doc1, sección 2.4)
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.db.database import get_db
from app.models.m7_m12_frontera import (
    CreditScore, CapitalTrabajo, PricingIntelligence,
    InversionAvanzada, AlertaFraude, BenchmarkSectorial
)
from app.services.ml_pipeline import get_ml_predictor

router = APIRouter(prefix="/api/v1/motors", tags=["M7-M12 Finanzas de Frontera"])


# ============= M7 - CRÉDITO Y SCORING =============

@router.post("/m7/credit-score", status_code=201)
def calcular_credit_score(
    empresa_id: int = Query(...),
    ingresos_anuales: float = Query(...),
    deuda_total: float = Query(...),
    historial_pago: float = Query(..., ge=0, le=1, description="0=malo, 1=excelente"),
    db: Session = Depends(get_db)
):
    """M7: Calcular score crediticio con datos alternativos (dictamen informativo)"""
    # Modelo simple de scoring
    ratio_deuda = deuda_total / (ingresos_anuales + 1)
    score = max(0, min(1000, 1000 * (0.4 * historial_pago + 0.6 * (1 - min(ratio_deuda, 1)))))

    if score >= 800:
        rating, pd = "AAA", 0.01
    elif score >= 700:
        rating, pd = "AA", 0.03
    elif score >= 600:
        rating, pd = "A", 0.07
    elif score >= 500:
        rating, pd = "BBB", 0.15
    else:
        rating, pd = "BB", 0.30

    cs = CreditScore(
        empresa_id=empresa_id, fecha=date.today(), score=score,
        rating=rating, probabilidad_default=pd, capacidad_pago=ingresos_anuales - deuda_total,
        dictamen="Dictamen de carácter exclusivamente informativo (Doc1)."
    )
    db.add(cs)
    db.commit()
    db.refresh(cs)

    return {
        "empresa_id": empresa_id, "score": round(score, 1), "rating": rating,
        "probabilidad_default": pd, "ratio_deuda_ingresos": round(ratio_deuda, 3),
        "dictamen": cs.dictamen
    }


# ============= M8 - CAPITAL DE TRABAJO =============

@router.post("/m8/capital-trabajo", status_code=201)
def analizar_capital_trabajo(
    empresa_id: int = Query(...),
    dias_inventario: float = Query(...),
    dias_cobro: float = Query(...),
    dias_pago: float = Query(...),
    db: Session = Depends(get_db)
):
    """M8: Analizar ciclo de conversión de efectivo (CCC)"""
    ccc = dias_inventario + dias_cobro - dias_pago

    if ccc < 30:
        recom = "Excelente: ciclo de efectivo muy eficiente"
    elif ccc < 60:
        recom = "Bueno: margen de mejora en cobros o inventario"
    else:
        recom = "Atención: ciclo largo, optimizar cobros y rotación de inventario"

    ct = CapitalTrabajo(
        empresa_id=empresa_id, fecha=date.today(),
        dias_inventario=dias_inventario, dias_cobro=dias_cobro, dias_pago=dias_pago,
        ciclo_conversion_efectivo=ccc, capital_trabajo_neto=0.0, recomendacion=recom
    )
    db.add(ct)
    db.commit()

    return {
        "empresa_id": empresa_id, "ciclo_conversion_efectivo": round(ccc, 1),
        "dias_inventario": dias_inventario, "dias_cobro": dias_cobro,
        "dias_pago": dias_pago, "recomendacion": recom
    }


# ============= M9 - PRICING =============

@router.post("/m9/pricing", status_code=201)
def analizar_pricing(
    empresa_id: int = Query(...),
    producto: str = Query(...),
    precio_actual: float = Query(...),
    costo_unitario: float = Query(...),
    elasticidad: float = Query(-1.5, description="Elasticidad precio-demanda"),
    db: Session = Depends(get_db)
):
    """M9: Sugerir precio óptimo (dictamen informativo)"""
    # Precio óptimo simplificado basado en elasticidad y markup
    margen_actual = (precio_actual - costo_unitario) / precio_actual if precio_actual > 0 else 0
    # Markup óptimo según elasticidad: P = C * e/(e+1)
    if elasticidad < -1:
        precio_optimo = costo_unitario * (elasticidad / (elasticidad + 1))
    else:
        precio_optimo = precio_actual

    pi = PricingIntelligence(
        empresa_id=empresa_id, producto=producto, fecha=date.today(),
        precio_actual=precio_actual, precio_optimo_sugerido=precio_optimo,
        elasticidad_precio=elasticidad, margen_actual=margen_actual,
        dictamen="Dictamen de carácter exclusivamente informativo (Doc1)."
    )
    db.add(pi)
    db.commit()

    return {
        "producto": producto, "precio_actual": precio_actual,
        "precio_optimo_sugerido": round(precio_optimo, 2),
        "margen_actual_pct": round(margen_actual * 100, 1),
        "variacion_sugerida_pct": round((precio_optimo - precio_actual) / precio_actual * 100, 1) if precio_actual > 0 else 0,
        "dictamen": pi.dictamen
    }


# ============= M10 - INVERSIONES =============

@router.post("/m10/inversiones", status_code=201)
def registrar_inversion(
    empresa_id: int = Query(...),
    instrumento: str = Query(...),
    tipo: str = Query(...),
    monto: float = Query(...),
    tasa_esperada: float = Query(...),
    db: Session = Depends(get_db)
):
    """M10: Registrar inversión y proyectar retorno"""
    inv = InversionAvanzada(
        empresa_id=empresa_id, instrumento=instrumento, tipo=tipo,
        monto_invertido=monto, fecha_inicio=date.today(),
        tasa_esperada=tasa_esperada,
        riesgo="bajo" if tasa_esperada < 0.1 else "medio" if tasa_esperada < 0.3 else "alto"
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)

    return {
        "id": inv.id, "instrumento": instrumento, "monto": monto,
        "tasa_esperada": tasa_esperada, "riesgo": inv.riesgo,
        "retorno_proyectado_anual": round(monto * tasa_esperada, 2)
    }


@router.get("/m10/inversiones/{empresa_id}")
def listar_inversiones(empresa_id: int, db: Session = Depends(get_db)):
    """M10: Portafolio de inversiones activas"""
    invs = db.query(InversionAvanzada).filter(
        InversionAvanzada.empresa_id == empresa_id,
        InversionAvanzada.estado == "activa"
    ).all()
    total = sum(i.monto_invertido for i in invs)
    return {
        "empresa_id": empresa_id, "total_invertido": total,
        "cantidad": len(invs),
        "inversiones": [
            {"instrumento": i.instrumento, "monto": i.monto_invertido,
             "tasa": i.tasa_esperada, "riesgo": i.riesgo} for i in invs
        ]
    }


# ============= M11 - FRAUDE =============

@router.post("/m11/detectar-fraude")
def detectar_fraude(
    empresa_id: int = Query(...),
    transacciones: List[float] = Query(..., description="Serie de montos de transacciones"),
    db: Session = Depends(get_db)
):
    """M11: Detectar anomalías/fraude en transacciones usando ML"""
    predictor = get_ml_predictor()
    resultado = predictor.detect_anomalies(transacciones, threshold=2.0)

    # Registrar alertas detectadas
    alertas_creadas = 0
    for anom in resultado.get("anomalies", []):
        severidad = "critica" if anom["severity"] == "high" else "media"
        alerta = AlertaFraude(
            empresa_id=empresa_id, fecha_deteccion=date.today(),
            tipo_anomalia="Monto atípico", severidad=severidad,
            score_riesgo=min(1.0, anom["z_score"] / 5),
            monto_involucrado=anom["value"],
            descripcion=f"Z-score: {anom['z_score']:.2f}"
        )
        db.add(alerta)
        alertas_creadas += 1
    db.commit()

    return {
        "empresa_id": empresa_id,
        "total_anomalias": resultado.get("total_anomalias", resultado.get("total_anomalies", 0)),
        "alertas_registradas": alertas_creadas,
        "detalle": resultado.get("anomalies", [])
    }


@router.get("/m11/alertas/{empresa_id}")
def listar_alertas(empresa_id: int, db: Session = Depends(get_db)):
    """M11: Alertas de fraude abiertas"""
    alertas = db.query(AlertaFraude).filter(
        AlertaFraude.empresa_id == empresa_id,
        AlertaFraude.estado == "abierta"
    ).all()
    return {
        "empresa_id": empresa_id, "alertas_abiertas": len(alertas),
        "alertas": [
            {"id": a.id, "tipo": a.tipo_anomalia, "severidad": a.severidad,
             "score": a.score_riesgo, "monto": a.monto_involucrado} for a in alertas
        ]
    }


# ============= M12 - BENCHMARKING SECTORIAL =============

@router.post("/m12/benchmark", status_code=201)
def benchmark_sectorial(
    empresa_id: int = Query(...),
    sector: str = Query(...),
    metrica: str = Query(...),
    valor_empresa: float = Query(...),
    mediana_sector: float = Query(...),
    db: Session = Depends(get_db)
):
    """M12: Comparar empresa contra su sector (benchmarking anónimo)"""
    # Posición relativa
    if valor_empresa >= mediana_sector * 1.2:
        posicion, percentil = "lider", 90
    elif valor_empresa >= mediana_sector:
        posicion, percentil = "sobre_media", 65
    elif valor_empresa >= mediana_sector * 0.8:
        posicion, percentil = "media", 45
    else:
        posicion, percentil = "bajo_media", 25

    bench = BenchmarkSectorial(
        empresa_id=empresa_id, sector=sector, fecha=date.today(),
        metrica=metrica, valor_empresa=valor_empresa,
        percentil_sector=percentil, mediana_sector=mediana_sector,
        posicion=posicion,
        insight=f"La empresa está {posicion.replace('_', ' ')} respecto al sector {sector}"
    )
    db.add(bench)
    db.commit()

    return {
        "empresa_id": empresa_id, "sector": sector, "metrica": metrica,
        "valor_empresa": valor_empresa, "mediana_sector": mediana_sector,
        "percentil": percentil, "posicion": posicion, "insight": bench.insight
    }

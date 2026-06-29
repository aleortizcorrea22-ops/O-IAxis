"""
API routes for M1, M3, M4, M6 financial motors
M1: Control Operativo, M3: Flujos Internos, M4: Macro, M6: Patrimonio
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List

from app.db.database import get_db

# M1 - Control Operativo
from app.models.m1_control_operativo import IndicadorOperacional, MetricaDesempenio
# M3 - Flujos Internos
from app.models.m3_flujos_internos import FlujoInterno, RotacionFondos, AsignacionPresupuestaria
# M4 - Contexto Macroeconómico
from app.models.m4_macro import IndicadorMacroeconomico, ImpactoMacroEmpresa, EscenarioMacro
# M6 - Patrimonio
from app.models.m6_patrimonio import Activo, Pasivo, EstadoPatrimonial, RatiosCapital

router = APIRouter(prefix="/api/v1/motors", tags=["M1-M3-M4-M6"])


# ============= M1 - CONTROL OPERATIVO =============

@router.post("/m1/indicadores", status_code=201)
def create_indicador_m1(
    empresa_id: int = Query(...),
    area: str = Query(...),
    nombre: str = Query(...),
    valor: float = Query(...),
    db: Session = Depends(get_db)
):
    """Crear indicador operacional"""
    from datetime import date
    indicador = IndicadorOperacional(
        empresa_id=empresa_id,
        area=area,
        fecha=date.today(),
        nombre_indicador=nombre,
        valor_actual=valor,
        variacion_porcentaje=0.0
    )
    db.add(indicador)
    db.commit()
    db.refresh(indicador)
    return {"id": indicador.id, "status": "created"}


@router.get("/m1/indicadores")
def list_indicadores_m1(
    empresa_id: int = Query(...),
    area: str = Query(None),
    db: Session = Depends(get_db)
):
    """Listar indicadores operacionales"""
    query = db.query(IndicadorOperacional).filter(
        IndicadorOperacional.empresa_id == empresa_id
    )
    if area:
        query = query.filter(IndicadorOperacional.area == area)

    return [
        {
            "id": i.id,
            "area": str(i.area),
            "fecha": i.fecha,
            "nombre": i.nombre_indicador,
            "valor": i.valor_actual,
            "estado": i.estado
        }
        for i in query.all()
    ]


@router.get("/m1/metricas/{empresa_id}")
def get_metricas_desempenio(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener métricas de desempeño"""
    metrica = db.query(MetricaDesempenio).filter(
        MetricaDesempenio.empresa_id == empresa_id
    ).order_by(MetricaDesempenio.fecha.desc()).first()

    if not metrica:
        return {"empresa_id": empresa_id, "message": "No hay métricas registradas"}

    return {
        "empresa_id": empresa_id,
        "fecha": metrica.fecha,
        "eficiencia": metrica.eficiencia_operativa,
        "calidad": metrica.calidad_procesos,
        "cumplimiento_sla": metrica.cumplimiento_sla,
        "productividad": metrica.productividad,
        "tendencia": metrica.tendencia
    }


# ============= M3 - FLUJOS INTERNOS =============

@router.post("/m3/flujos", status_code=201)
def create_flujo_interno(
    empresa_id: int = Query(...),
    tipo_flujo: str = Query(...),
    monto: float = Query(...),
    fecha: str = Query(...),
    db: Session = Depends(get_db)
):
    """Crear flujo interno"""
    from datetime import datetime
    flujo = FlujoInterno(
        empresa_id=empresa_id,
        tipo_flujo=tipo_flujo,
        monto=monto,
        fecha_programada=datetime.fromisoformat(fecha).date(),
        referencia=f"FLUJO_{empresa_id}_{datetime.now().timestamp()}"
    )
    db.add(flujo)
    db.commit()
    return {"id": flujo.id, "status": "created"}


@router.get("/m3/flujos")
def list_flujos_internos(
    empresa_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Listar flujos internos"""
    flujos = db.query(FlujoInterno).filter(
        FlujoInterno.empresa_id == empresa_id
    ).all()

    return [
        {
            "id": f.id,
            "tipo": str(f.tipo_flujo),
            "monto": f.monto,
            "fecha": f.fecha_programada,
            "estado": f.estado
        }
        for f in flujos
    ]


@router.get("/m3/rotacion/{empresa_id}")
def get_rotacion_fondos(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener rotación de fondos"""
    rotacion = db.query(RotacionFondos).filter(
        RotacionFondos.empresa_id == empresa_id
    ).order_by(RotacionFondos.fecha.desc()).first()

    if not rotacion:
        return {"empresa_id": empresa_id, "message": "No hay datos de rotación"}

    return {
        "empresa_id": empresa_id,
        "fecha": rotacion.fecha,
        "dias_rotacion": rotacion.dias_rotacion,
        "monto_rotado": rotacion.monto_rotado,
        "eficiencia": rotacion.eficiencia
    }


# ============= M4 - CONTEXTO MACROECONÓMICO =============

@router.post("/m4/indicadores-macro", status_code=201)
def create_indicador_macro(
    variable: str = Query(...),
    valor: float = Query(...),
    db: Session = Depends(get_db)
):
    """Crear indicador macroeconómico"""
    from datetime import date
    indicador = IndicadorMacroeconomico(
        variable=variable,
        fecha=date.today(),
        valor=valor
    )
    db.add(indicador)
    db.commit()
    return {"id": indicador.id, "status": "created"}


@router.get("/m4/indicadores-macro")
def list_indicadores_macro(
    variable: str = Query(None),
    db: Session = Depends(get_db)
):
    """Listar indicadores macroeconómicos"""
    query = db.query(IndicadorMacroeconomico)
    if variable:
        query = query.filter(IndicadorMacroeconomico.variable == variable)

    return [
        {
            "variable": str(i.variable),
            "fecha": i.fecha,
            "valor": i.valor,
            "variacion_mes": i.variacion_mes,
            "proyeccion": i.proyeccion
        }
        for i in query.order_by(IndicadorMacroeconomico.fecha.desc()).limit(20).all()
    ]


@router.get("/m4/impacto/{empresa_id}")
def get_impacto_macro(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener impacto macroeconomico en empresa"""
    impactos = db.query(ImpactoMacroEmpresa).filter(
        ImpactoMacroEmpresa.empresa_id == empresa_id
    ).order_by(ImpactoMacroEmpresa.fecha.desc()).limit(5).all()

    return [
        {
            "variable": str(i.variable_macro),
            "fecha": i.fecha,
            "impacto": i.impacto_esperado,
            "magnitud": i.magnitud_impacto,
            "areas_afectadas": i.areas_afectadas
        }
        for i in impactos
    ]


# ============= M6 - PATRIMONIO =============

@router.post("/m6/activos", status_code=201)
def create_activo(
    empresa_id: int = Query(...),
    tipo_activo: str = Query(...),
    descripcion: str = Query(...),
    valor: float = Query(...),
    db: Session = Depends(get_db)
):
    """Registrar activo"""
    activo = Activo(
        empresa_id=empresa_id,
        tipo_activo=tipo_activo,
        descripcion=descripcion,
        valor_libro=valor,
        valor_mercado=valor
    )
    db.add(activo)
    db.commit()
    return {"id": activo.id, "status": "created"}


@router.get("/m6/activos/{empresa_id}")
def list_activos(empresa_id: int, db: Session = Depends(get_db)):
    """Listar activos de empresa"""
    activos = db.query(Activo).filter(
        Activo.empresa_id == empresa_id,
        Activo.activo == True
    ).all()

    total = sum(a.valor_libro for a in activos)

    return {
        "empresa_id": empresa_id,
        "total_activos": total,
        "cantidad": len(activos),
        "activos": [
            {
                "id": a.id,
                "tipo": str(a.tipo_activo),
                "descripcion": a.descripcion,
                "valor_libro": a.valor_libro,
                "valor_mercado": a.valor_mercado
            }
            for a in activos
        ]
    }


@router.delete("/m6/activos/{activo_id}", status_code=204)
def delete_activo(activo_id: int, db: Session = Depends(get_db)):
    """Borrar activo"""
    from fastapi import HTTPException
    activo = db.query(Activo).filter(Activo.id == activo_id).first()
    if not activo:
        raise HTTPException(status_code=404, detail="Activo not found")
    db.delete(activo)
    db.commit()


@router.get("/m6/balance/{empresa_id}")
def get_estado_patrimonial(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener estado patrimonial"""
    balance = db.query(EstadoPatrimonial).filter(
        EstadoPatrimonial.empresa_id == empresa_id
    ).order_by(EstadoPatrimonial.fecha.desc()).first()

    if not balance:
        return {"empresa_id": empresa_id, "message": "No hay balance registrado"}

    return {
        "empresa_id": empresa_id,
        "fecha": balance.fecha,
        "activos": balance.total_activos,
        "pasivos": balance.total_pasivos,
        "patrimonio": balance.patrimonio,
        "activos_corrientes": balance.activos_corrientes,
        "activos_no_corrientes": balance.activos_no_corrientes
    }

"""
API routes for M5 Fiscal (Tax Management)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List

from app.db.database import get_db
from app.models.m5_fiscal import ImpuestoDetalle, FiscalObligacion, RetencionesCobradas, ResultadoFiscalProyectado
from app.api.schemas.m5_fiscal import (
    ImpuestoDetalleCreate, ImpuestoDetalleResponse,
    FiscalObligacionCreate, FiscalObligacionResponse,
    RetencionesCobradas​Create, RetencionesCobradas​Response,
    ResultadoFiscalProyectadoCreate, ResultadoFiscalProyectadoResponse,
    FiscalResumenResponse
)

router = APIRouter(prefix="/api/v1/motors/m5", tags=["M5 - Fiscal"])


# ============= IMPUESTOS =============

@router.post("/impuestos", response_model=ImpuestoDetalleResponse, status_code=201)
def create_impuesto(
    impuesto: ImpuestoDetalleCreate,
    db: Session = Depends(get_db)
):
    """Crear detalle de impuesto"""
    monto_calculado = impuesto.base_imponible * (impuesto.alicuota / 100)

    db_impuesto = ImpuestoDetalle(
        **impuesto.dict(),
        monto_impuesto=monto_calculado
    )
    db.add(db_impuesto)
    db.commit()
    db.refresh(db_impuesto)
    return db_impuesto


@router.get("/impuestos/{impuesto_id}", response_model=ImpuestoDetalleResponse)
def get_impuesto(impuesto_id: int, db: Session = Depends(get_db)):
    """Obtener detalle de impuesto"""
    impuesto = db.query(ImpuestoDetalle).filter(
        ImpuestoDetalle.id == impuesto_id
    ).first()
    if not impuesto:
        raise HTTPException(status_code=404, detail="Impuesto not found")
    return impuesto


@router.get("/impuestos", response_model=List[ImpuestoDetalleResponse])
def list_impuestos(
    empresa_id: int = Query(...),
    estado: str = Query(None),
    db: Session = Depends(get_db)
):
    """Listar impuestos de una empresa"""
    query = db.query(ImpuestoDetalle).filter(
        ImpuestoDetalle.empresa_id == empresa_id
    )
    if estado:
        query = query.filter(ImpuestoDetalle.estado == estado)

    return query.all()


@router.put("/impuestos/{impuesto_id}", response_model=ImpuestoDetalleResponse)
def update_impuesto(
    impuesto_id: int,
    impuesto_update: ImpuestoDetalleCreate,
    db: Session = Depends(get_db)
):
    """Actualizar impuesto"""
    db_impuesto = db.query(ImpuestoDetalle).filter(
        ImpuestoDetalle.id == impuesto_id
    ).first()
    if not db_impuesto:
        raise HTTPException(status_code=404, detail="Impuesto not found")

    for key, value in impuesto_update.dict().items():
        setattr(db_impuesto, key, value)

    db.commit()
    db.refresh(db_impuesto)
    return db_impuesto


# ============= OBLIGACIONES FISCALES =============

@router.post("/obligaciones", response_model=FiscalObligacionResponse, status_code=201)
def create_obligacion(
    obligacion: FiscalObligacionCreate,
    db: Session = Depends(get_db)
):
    """Crear obligación fiscal"""
    db_obligacion = FiscalObligacion(**obligacion.dict())
    db.add(db_obligacion)
    db.commit()
    db.refresh(db_obligacion)
    return db_obligacion


@router.get("/obligaciones", response_model=List[FiscalObligacionResponse])
def list_obligaciones(
    empresa_id: int = Query(...),
    estatus: str = Query(None),
    db: Session = Depends(get_db)
):
    """Listar obligaciones fiscales"""
    query = db.query(FiscalObligacion).filter(
        FiscalObligacion.empresa_id == empresa_id
    )
    if estatus:
        query = query.filter(FiscalObligacion.estatus == estatus)

    return query.all()


@router.put("/obligaciones/{obligacion_id}", response_model=FiscalObligacionResponse)
def update_obligacion(
    obligacion_id: int,
    obligacion_update: FiscalObligacionCreate,
    db: Session = Depends(get_db)
):
    """Actualizar obligación fiscal"""
    db_obligacion = db.query(FiscalObligacion).filter(
        FiscalObligacion.id == obligacion_id
    ).first()
    if not db_obligacion:
        raise HTTPException(status_code=404, detail="Obligación not found")

    for key, value in obligacion_update.dict().items():
        setattr(db_obligacion, key, value)

    db.commit()
    db.refresh(db_obligacion)
    return db_obligacion


# ============= RETENCIONES COBRADAS =============

@router.post("/retenciones", response_model=RetencionesCobradas​Response, status_code=201)
def create_retencion(
    retencion: RetencionesCobradas​Create,
    db: Session = Depends(get_db)
):
    """Registrar retención cobrada"""
    db_retencion = RetencionesCobradas(**retencion.dict())
    db.add(db_retencion)
    db.commit()
    db.refresh(db_retencion)
    return db_retencion


@router.get("/retenciones", response_model=List[RetencionesCobradas​Response])
def list_retenciones(
    empresa_id: int = Query(...),
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    db: Session = Depends(get_db)
):
    """Listar retenciones cobradas"""
    retenciones = db.query(RetencionesCobradas).filter(
        RetencionesCobradas.empresa_id == empresa_id,
        RetencionesCobradas.fecha >= fecha_inicio,
        RetencionesCobradas.fecha <= fecha_fin
    ).all()
    return retenciones


# ============= PROYECCIONES =============

@router.post("/proyecciones", response_model=ResultadoFiscalProyectadoResponse, status_code=201)
def create_proyeccion(
    proyeccion: ResultadoFiscalProyectadoCreate,
    db: Session = Depends(get_db)
):
    """Crear proyección de resultado fiscal"""
    resultado_neto = (proyeccion.ingresos_proyectados -
                     proyeccion.gastos_proyectados -
                     proyeccion.impuestos_estimados)

    tasa_efectiva = (proyeccion.impuestos_estimados / proyeccion.ingresos_proyectados * 100
                    if proyeccion.ingresos_proyectados > 0 else 0)

    db_proyeccion = ResultadoFiscalProyectado(
        **proyeccion.dict(),
        resultado_neto=resultado_neto,
        tasa_efectiva_impositiva=tasa_efectiva
    )
    db.add(db_proyeccion)
    db.commit()
    db.refresh(db_proyeccion)
    return db_proyeccion


@router.get("/proyecciones/{empresa_id}", response_model=List[ResultadoFiscalProyectadoResponse])
def list_proyecciones(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    """Listar proyecciones fiscales"""
    proyecciones = db.query(ResultadoFiscalProyectado).filter(
        ResultadoFiscalProyectado.empresa_id == empresa_id
    ).all()
    return proyecciones


# ============= RESUMEN EJECUTIVO =============

@router.get("/resumen/{empresa_id}", response_model=FiscalResumenResponse)
def get_fiscal_resumen(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener resumen ejecutivo fiscal"""

    # Get pending taxes
    impuestos_pendientes = db.query(ImpuestoDetalle).filter(
        ImpuestoDetalle.empresa_id == empresa_id,
        ImpuestoDetalle.estado.in_(["pendiente", "vencido"])
    ).all()

    # Get upcoming obligations
    obligaciones = db.query(FiscalObligacion).filter(
        FiscalObligacion.empresa_id == empresa_id,
        FiscalObligacion.estatus == "pendiente",
        FiscalObligacion.fecha_vencimiento <= datetime.utcnow().date() + __import__('datetime').timedelta(days=30)
    ).all()

    # Calculate totals
    monto_adeudado = db.query(func.sum(ImpuestoDetalle.monto_impuesto - ImpuestoDetalle.monto_pagado)).filter(
        ImpuestoDetalle.empresa_id == empresa_id,
        ImpuestoDetalle.estado != "pagado"
    ).scalar() or 0.0

    retenciones_acumulado = db.query(func.sum(RetencionesCobradas.monto_retenido)).filter(
        RetencionesCobradas.empresa_id == empresa_id
    ).scalar() or 0.0

    # Get latest projection
    proyeccion = db.query(ResultadoFiscalProyectado).filter(
        ResultadoFiscalProyectado.empresa_id == empresa_id
    ).order_by(ResultadoFiscalProyectado.created_at.desc()).first()

    return FiscalResumenResponse(
        empresa_id=empresa_id,
        impuestos_pendientes=[ImpuestoDetalleResponse.from_orm(i) for i in impuestos_pendientes],
        obligaciones_proximas=[FiscalObligacionResponse.from_orm(o) for o in obligaciones],
        monto_total_adeudado=monto_adeudado,
        monto_retenciones_acumulado=retenciones_acumulado,
        proyeccion_anual=ResultadoFiscalProyectadoResponse.from_orm(proyeccion) if proyeccion else None,
        fecha_actualizacion=datetime.utcnow()
    )

"""
API routes for M2 Tesorería (Treasury Management)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List

from app.db.database import get_db
from app.models.m2_tesoreria import TesoreriaTransaction, CajaDiaria, FlujoCaja
from app.api.schemas.m2_tesoreria import (
    TesoreriaTransactionCreate, TesoreriaTransactionResponse,
    CajaDiariaCreate, CajaDiariaResponse,
    FlujoCajaCreate, FlujoCajaResponse,
    TesoreriaResumenResponse
)

router = APIRouter(prefix="/api/v1/motors/m2", tags=["M2 - Tesorería"])


# ============= TRANSACCIONES =============

@router.post("/transactions", response_model=TesoreriaTransactionResponse, status_code=201)
def create_transaction(
    transaction: TesoreriaTransactionCreate,
    db: Session = Depends(get_db)
):
    """Crear nueva transacción de tesorería"""

    # Check if referencia already exists
    existing = db.query(TesoreriaTransaction).filter(
        TesoreriaTransaction.referencia == transaction.referencia
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Referencia already exists")

    db_transaction = TesoreriaTransaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/transactions/{transaction_id}", response_model=TesoreriaTransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Obtener transacción por ID"""
    transaction = db.query(TesoreriaTransaction).filter(
        TesoreriaTransaction.id == transaction_id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/transactions", response_model=List[TesoreriaTransactionResponse])
def list_transactions(
    empresa_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Listar transacciones de una empresa"""
    transactions = db.query(TesoreriaTransaction).filter(
        TesoreriaTransaction.empresa_id == empresa_id
    ).offset(skip).limit(limit).all()
    return transactions


@router.put("/transactions/{transaction_id}", response_model=TesoreriaTransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TesoreriaTransactionCreate,
    db: Session = Depends(get_db)
):
    """Actualizar transacción"""
    db_transaction = db.query(TesoreriaTransaction).filter(
        TesoreriaTransaction.id == transaction_id
    ).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction_update.dict().items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.delete("/transactions/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Eliminar transacción"""
    db_transaction = db.query(TesoreriaTransaction).filter(
        TesoreriaTransaction.id == transaction_id
    ).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(db_transaction)
    db.commit()


# ============= CAJA DIARIA =============

@router.post("/caja-diaria", response_model=CajaDiariaResponse, status_code=201)
def create_caja_diaria(
    caja: CajaDiariaCreate,
    db: Session = Depends(get_db)
):
    """Crear registro de caja diaria"""
    # Check if already exists for this date
    existing = db.query(CajaDiaria).filter(
        CajaDiaria.empresa_id == caja.empresa_id,
        CajaDiaria.fecha == caja.fecha
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Caja diaria already exists for this date")

    saldo_final = caja.saldo_inicial + caja.ingresos - caja.egresos
    db_caja = CajaDiaria(
        **caja.dict(),
        saldo_final=saldo_final
    )
    db.add(db_caja)
    db.commit()
    db.refresh(db_caja)
    return db_caja


@router.get("/caja-diaria", response_model=List[CajaDiariaResponse])
def list_caja_diaria(
    empresa_id: int = Query(...),
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    db: Session = Depends(get_db)
):
    """Listar caja diaria para un rango de fechas"""
    cajas = db.query(CajaDiaria).filter(
        CajaDiaria.empresa_id == empresa_id,
        CajaDiaria.fecha >= fecha_inicio,
        CajaDiaria.fecha <= fecha_fin
    ).all()
    return cajas


# ============= FLUJO DE CAJA =============

@router.post("/flujo-caja", response_model=FlujoCajaResponse, status_code=201)
def create_flujo_caja(
    flujo: FlujoCajaCreate,
    db: Session = Depends(get_db)
):
    """Crear proyección de flujo de caja"""
    db_flujo = FlujoCaja(**flujo.dict())
    db.add(db_flujo)
    db.commit()
    db.refresh(db_flujo)
    return db_flujo


@router.get("/flujo-caja", response_model=List[FlujoCajaResponse])
def list_flujo_caja(
    empresa_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Listar proyecciones de flujo de caja"""
    flujos = db.query(FlujoCaja).filter(
        FlujoCaja.empresa_id == empresa_id,
        FlujoCaja.estado == "activo"
    ).all()
    return flujos


# ============= RESUMEN EJECUTIVO =============

@router.get("/resumen/{empresa_id}", response_model=TesoreriaResumenResponse)
def get_tesoreria_resumen(empresa_id: int, db: Session = Depends(get_db)):
    """Obtener resumen ejecutivo de tesorería"""

    # Get latest caja diaria
    latest_caja = db.query(CajaDiaria).filter(
        CajaDiaria.empresa_id == empresa_id
    ).order_by(CajaDiaria.fecha.desc()).first()

    saldo_actual = latest_caja.saldo_final if latest_caja else 0.0

    # Get current month transactions
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)

    ingresos_mes = db.query(func.sum(TesoreriaTransaction.monto)).filter(
        TesoreriaTransaction.empresa_id == empresa_id,
        TesoreriaTransaction.tipo == "ingresos",
        TesoreriaTransaction.fecha_transaccion >= month_start
    ).scalar() or 0.0

    egresos_mes = db.query(func.sum(TesoreriaTransaction.monto)).filter(
        TesoreriaTransaction.empresa_id == empresa_id,
        TesoreriaTransaction.tipo == "egresos",
        TesoreriaTransaction.fecha_transaccion >= month_start
    ).scalar() or 0.0

    # Get pending transactions count
    pendientes = db.query(func.count(TesoreriaTransaction.id)).filter(
        TesoreriaTransaction.empresa_id == empresa_id,
        TesoreriaTransaction.status == "pendiente"
    ).scalar() or 0

    # Get active flow projections
    flujos = db.query(FlujoCaja).filter(
        FlujoCaja.empresa_id == empresa_id,
        FlujoCaja.estado == "activo"
    ).all()

    return TesoreriaResumenResponse(
        empresa_id=empresa_id,
        saldo_actual=saldo_actual,
        ingresos_mes=ingresos_mes,
        egresos_mes=egresos_mes,
        flujo_neto=ingresos_mes - egresos_mes,
        proyeccion_flujo=[FlujoCajaResponse.from_orm(f) for f in flujos],
        transacciones_pendientes=pendientes,
        fecha_actualizacion=datetime.utcnow()
    )

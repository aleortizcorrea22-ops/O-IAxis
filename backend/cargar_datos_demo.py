"""
Carga datos demo en la BD de O-IAxis para testing
Ejecutar: python cargar_datos_demo.py
"""

import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

sys.path.insert(0, '.')

from app.db.database import SessionLocal, Base, engine
from app.models.m2_tesoreria import TesoreriaTransaction, TransactionType, TransactionStatus
from app.models.m5_fiscal import ImpuestoDetalle, TaxType
from app.models.m6_patrimonio import Activo, Pasivo, TipoActivo, TipoPasivo

# Asegurar que las tablas existan
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    print("Cargando datos demo...")

    # ===== M2 TESORERÍA =====
    txs = [
        TesoreriaTransaction(
            empresa_id=1,
            tipo=TransactionType.INGRESOS,
            monto=850000,
            referencia="Cobranza cliente ABC",
            fecha_transaccion=datetime.now() - timedelta(days=15),
            status=TransactionStatus.EJECUTADA,
        ),
        TesoreriaTransaction(
            empresa_id=1,
            tipo=TransactionType.INGRESOS,
            monto=620000,
            referencia="Cobranza cliente XYZ",
            fecha_transaccion=datetime.now() - timedelta(days=10),
            status=TransactionStatus.EJECUTADA,
        ),
        TesoreriaTransaction(
            empresa_id=1,
            tipo=TransactionType.EGRESOS,
            monto=250000,
            referencia="Pago proveedores",
            fecha_transaccion=datetime.now() - timedelta(days=8),
            status=TransactionStatus.EJECUTADA,
        ),
        TesoreriaTransaction(
            empresa_id=1,
            tipo=TransactionType.INGRESOS,
            monto=1200000,
            referencia="Cobranza proyecto especial",
            fecha_transaccion=datetime.now() - timedelta(days=5),
            status=TransactionStatus.EJECUTADA,
        ),
        TesoreriaTransaction(
            empresa_id=1,
            tipo=TransactionType.EGRESOS,
            monto=180000,
            referencia="Nomina de sueldos",
            fecha_transaccion=datetime.now() - timedelta(days=3),
            status=TransactionStatus.EJECUTADA,
        ),
        TesoreriaTransaction(
            empresa_id=1,
            tipo=TransactionType.EGRESOS,
            monto=95000,
            referencia="Servicios e infraestructura",
            fecha_transaccion=datetime.now() - timedelta(days=1),
            status=TransactionStatus.PENDIENTE,
        ),
    ]
    db.add_all(txs)
    print(f"[OK] {len(txs)} transacciones M2")

    # ===== M5 FISCAL =====
    impuestos = [
        ImpuestoDetalle(
            empresa_id=1,
            tipo_impuesto=TaxType.IVA,
            periodo="202606",
            base_imponible=500000,
            alicuota=0.21,
            fecha_vencimiento=datetime.now() - timedelta(days=5),
        ),
        ImpuestoDetalle(
            empresa_id=1,
            tipo_impuesto=TaxType.INGRESOS_BRUTOS,
            periodo="202606",
            base_imponible=850000,
            alicuota=0.05,
            fecha_vencimiento=datetime.now() - timedelta(days=3),
        ),
        ImpuestoDetalle(
            empresa_id=1,
            tipo_impuesto=TaxType.GANANCIAS,
            periodo="202606",
            base_imponible=320000,
            alicuota=0.30,
            fecha_vencimiento=datetime.now() + timedelta(days=20),
        ),
    ]
    db.add_all(impuestos)
    print(f"[OK] {len(impuestos)} registros fiscales M5")

    # ===== M6 PATRIMONIO =====
    activos = [
        Activo(
            empresa_id=1,
            tipo_activo=TipoActivo.BIENES_INMUEBLES,
            descripcion="Oficina central - CABA",
            valor_libro=5000000,
            valor_mercado=7200000,
            activo=True
        ),
        Activo(
            empresa_id=1,
            tipo_activo=TipoActivo.VEHICULOS,
            descripcion="Camion de reparto 2022",
            valor_libro=850000,
            valor_mercado=720000,
            activo=True
        ),
        Activo(
            empresa_id=1,
            tipo_activo=TipoActivo.MAQUINARIA,
            descripcion="Maquina de produccion CNC",
            valor_libro=1200000,
            valor_mercado=950000,
            activo=True
        ),
        Activo(
            empresa_id=1,
            tipo_activo=TipoActivo.INTANGIBLES,
            descripcion="Servidores y network",
            valor_libro=320000,
            valor_mercado=180000,
            activo=True
        ),
        Activo(
            empresa_id=1,
            tipo_activo=TipoActivo.INVERSIONES,
            descripcion="Muebles y equipamiento oficina",
            valor_libro=150000,
            valor_mercado=80000,
            activo=True
        ),
    ]
    db.add_all(activos)
    print(f"[OK] {len(activos)} activos M6")

    # ===== M6 PASIVOS =====
    pasivos = [
        Pasivo(
            empresa_id=1,
            tipo_pasivo=TipoPasivo.PRESTAMOS_LARGO_PLAZO,
            descripcion="Prestamo Banco Galicia - 36 meses",
            monto_total=2500000,
            tasa_interes=0.125,
            fecha_vencimiento=datetime.now() + timedelta(days=1095),
            plazo_meses=36,
            acreedor="Banco Galicia"
        ),
        Pasivo(
            empresa_id=1,
            tipo_pasivo=TipoPasivo.CUENTAS_POR_PAGAR,
            descripcion="Credito proveedor materias primas",
            monto_total=450000,
            tasa_interes=0.08,
            fecha_vencimiento=datetime.now() + timedelta(days=90),
            acreedor="Proveedor ABC SA"
        ),
    ]
    db.add_all(pasivos)
    print(f"[OK] {len(pasivos)} pasivos M6")

    db.commit()
    print("\n[OK] Datos demo cargados exitosamente")
    print("\nResumen:")
    print(f"  - M2 Tesoreria: 6 transacciones (~$2.8M flujo)")
    print(f"  - M5 Fiscal: 3 periodos de impuestos (~$243K)")
    print(f"  - M6 Patrimonio: 5 activos ($7.5M) + 2 pasivos ($2.95M)")
    print("\nAhora el Dashboard y todas las paginas tienen datos.")

except Exception as e:
    print(f"[ERROR] {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()

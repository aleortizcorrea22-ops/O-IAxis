"""
Auto-seed demo data if database is empty
Ejecuta automáticamente al iniciar si hay 0 registros
"""

from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.m2_tesoreria import TesoreriaTransaction, TransactionType, TransactionStatus
from app.models.m5_fiscal import ImpuestoDetalle, TaxType
from app.models.m6_patrimonio import Activo, Pasivo


def seed_demo_data():
    """Carga datos demo si la BD está vacía"""
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        if db.query(TesoreriaTransaction).count() > 0:
            return  # Ya hay datos, no cargar

        print("[SEED] Cargando datos demo...")

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
        print(f"  [OK] 6 transacciones M2")

        # ===== M5 FISCAL =====
        impuestos = [
            ImpuestoDetalle(
                empresa_id=1,
                tipo_impuesto=TaxType.IVA,
                periodo="202606",
                base_imponible=500000,
                alicuota=0.21,
                monto_impuesto=105000,
                fecha_vencimiento=datetime.now() - timedelta(days=5),
            ),
            ImpuestoDetalle(
                empresa_id=1,
                tipo_impuesto=TaxType.INGRESOS_BRUTOS,
                periodo="202606",
                base_imponible=850000,
                alicuota=0.05,
                monto_impuesto=42500,
                fecha_vencimiento=datetime.now() - timedelta(days=3),
            ),
            ImpuestoDetalle(
                empresa_id=1,
                tipo_impuesto=TaxType.GANANCIAS,
                periodo="202606",
                base_imponible=320000,
                alicuota=0.30,
                monto_impuesto=96000,
                fecha_vencimiento=datetime.now() + timedelta(days=20),
            ),
        ]
        db.add_all(impuestos)
        print(f"  [OK] 3 impuestos M5")

        # ===== M6 PATRIMONIO - ACTIVOS =====
        activos = [
            Activo(
                empresa_id=1,
                tipo_activo="bienes_inmuebles",
                descripcion="Oficina central - CABA",
                valor_libro=5000000,
                valor_mercado=7200000,
                activo=True
            ),
            Activo(
                empresa_id=1,
                tipo_activo="vehiculos",
                descripcion="Camion de reparto 2022",
                valor_libro=850000,
                valor_mercado=720000,
                activo=True
            ),
            Activo(
                empresa_id=1,
                tipo_activo="maquinaria",
                descripcion="Maquina de produccion CNC",
                valor_libro=1200000,
                valor_mercado=950000,
                activo=True
            ),
            Activo(
                empresa_id=1,
                tipo_activo="intangibles",
                descripcion="Servidores y network",
                valor_libro=320000,
                valor_mercado=180000,
                activo=True
            ),
            Activo(
                empresa_id=1,
                tipo_activo="inversiones",
                descripcion="Muebles y equipamiento oficina",
                valor_libro=150000,
                valor_mercado=80000,
                activo=True
            ),
        ]
        db.add_all(activos)
        print(f"  [OK] 5 activos M6")

        # ===== M6 PATRIMONIO - PASIVOS =====
        pasivos = [
            Pasivo(
                empresa_id=1,
                tipo_pasivo="prestamos_lp",
                descripcion="Prestamo Banco Galicia - 36 meses",
                monto_total=2500000,
                tasa_interes=0.125,
                fecha_vencimiento=datetime.now() + timedelta(days=1095),
                plazo_meses=36,
                acreedor="Banco Galicia"
            ),
            Pasivo(
                empresa_id=1,
                tipo_pasivo="cuentas_por_pagar",
                descripcion="Credito proveedor materias primas",
                monto_total=450000,
                tasa_interes=0.08,
                fecha_vencimiento=datetime.now() + timedelta(days=90),
                acreedor="Proveedor ABC SA"
            ),
        ]
        db.add_all(pasivos)
        print(f"  [OK] 2 pasivos M6")

        db.commit()
        print("[SEED] Demo data loaded successfully!")
        print("  Total: 6 transacciones + 3 impuestos + 5 activos + 2 pasivos")

    except Exception as e:
        print(f"[SEED ERROR] {e}")
        db.rollback()
    finally:
        db.close()

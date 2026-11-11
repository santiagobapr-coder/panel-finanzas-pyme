"""Movimientos de ejemplo (inventados) de una pastelería artesanal: nov 2025 – oct 2026."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
meses = pd.period_range("2025-11", "2026-10", freq="M")
estacion = {11: 1.10, 12: 1.45, 1: 0.85, 2: 1.0, 3: 0.95, 4: 1.0, 5: 1.35, 6: 1.05, 7: 0.95, 8: 0.9, 9: 1.0, 10: 1.1}

rows = []
for i, m in enumerate(meses):
    crec = 1 + 0.018 * i
    f = estacion[m.month] * crec
    base = pd.Timestamp(m.start_time)
    # Ingresos
    ventas_mostrador = rng.normal(11_800_000, 500_000) * f
    pedidos_enc = rng.normal(6_200_000, 450_000) * f
    eventos = rng.normal(2_400_000, 700_000) * f * (1.8 if m.month in (12, 5) else 1)
    domicilios = rng.normal(3_100_000, 300_000) * f
    for cat, v in [("Ventas mostrador", ventas_mostrador), ("Pedidos por encargo", pedidos_enc),
                   ("Eventos y catering", eventos), ("Domicilios", domicilios)]:
        rows.append((base + pd.Timedelta(days=int(rng.integers(0, 27))), "Ingreso", cat, v))
    # Gastos variables (dependen de ventas)
    ventas_tot = ventas_mostrador + pedidos_enc + eventos + domicilios
    rows += [
        (base + pd.Timedelta(days=int(rng.integers(0, 27))), "Gasto", "Insumos y materia prima", ventas_tot * rng.normal(0.33, 0.015)),
        (base + pd.Timedelta(days=int(rng.integers(0, 27))), "Gasto", "Empaques", ventas_tot * rng.normal(0.045, 0.004)),
        (base + pd.Timedelta(days=int(rng.integers(0, 27))), "Gasto", "Comisiones y domicilios", ventas_tot * rng.normal(0.05, 0.005)),
    ]
    # Gastos fijos
    rows += [
        (base + pd.Timedelta(days=1), "Gasto", "Arriendo", 3_800_000),
        (base + pd.Timedelta(days=25), "Gasto", "Nómina", 7_400_000 + (500_000 if i >= 6 else 0)),
        (base + pd.Timedelta(days=15), "Gasto", "Servicios públicos", rng.normal(1_050_000, 90_000)),
        (base + pd.Timedelta(days=10), "Gasto", "Marketing", rng.normal(900_000, 150_000) * (1.4 if m.month in (11, 4) else 1)),
        (base + pd.Timedelta(days=20), "Gasto", "Mantenimiento", rng.normal(350_000, 120_000)),
    ]
    if m.month in (3, 9):
        rows.append((base + pd.Timedelta(days=12), "Gasto", "Equipos", 4_200_000))
    if m.month == 4:
        rows.append((base + pd.Timedelta(days=18), "Gasto", "Impuestos", 2_800_000))
df = pd.DataFrame(rows, columns=["fecha", "tipo", "categoria", "monto"])
df["monto"] = df["monto"].round(-3).astype(int)
df["fecha"] = df["fecha"].dt.date
df = df.sort_values("fecha")
df.to_csv("movimientos.csv", index=False)
print(len(df), "movimientos")

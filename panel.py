"""Panel de finanzas para negocios pequeños -> tablero.html"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dashboard_kit import PALETTE, SERIES, money, render_dashboard, table_html, tag

CAJA_INICIAL = 9_000_000  # saldo de caja al inicio del periodo (dato de ejemplo)
FIJOS = ["Arriendo", "Nómina", "Servicios públicos", "Marketing", "Mantenimiento"]
EXTRAS = ["Equipos", "Impuestos"]  # gastos no recurrentes

df = pd.read_csv("movimientos.csv", parse_dates=["fecha"])
df["mes"] = df.fecha.dt.to_period("M")

ing = df[df.tipo == "Ingreso"].groupby("mes")["monto"].sum()
gas = df[df.tipo == "Gasto"].groupby("mes")["monto"].sum()
m = pd.DataFrame({"ingresos": ing, "gastos": gas})
m["utilidad"] = m.ingresos - m.gastos
m["margen"] = m.utilidad / m.ingresos * 100
m["caja"] = CAJA_INICIAL + m.utilidad.cumsum()

# Punto de equilibrio mensual = costos fijos / margen de contribución
fijos_m = df[df.categoria.isin(FIJOS)].groupby("mes")["monto"].sum().mean()
variables = df[(df.tipo == "Gasto") & ~df.categoria.isin(FIJOS + EXTRAS)]["monto"].sum()
ingresos_tot = ing.sum()
mc = 1 - variables / ingresos_tot
equilibrio = fijos_m / mc

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
fm = lambda p: f"{MESES[p.month - 1]} {str(p.year)[2:]}"
etq = [fm(p) for p in m.index]

# Gráfico 1: ingresos vs gastos (arriba) y margen (abajo)
fig1, (ax, axm) = plt.subplots(2, 1, figsize=(7.6, 4.6), sharex=True, gridspec_kw={"height_ratios": [3, 1.2], "hspace": 0.12})
x = np.arange(len(m))
w = 0.38
ax.bar(x - w / 2, m.ingresos / 1e6, w, color=PALETTE["primary"], label="Ingresos")
ax.bar(x + w / 2, m.gastos / 1e6, w, color=PALETTE["accent"], label="Gastos")
ax.set_ylabel("Millones COP")
ax.set_title("Ingresos, gastos y margen por mes")
ax.grid(axis="x", visible=False)
ax.legend(frameon=False, ncol=2, loc="upper left")
ax.set_ylim(0, m[["ingresos", "gastos"]].max().max() / 1e6 * 1.2)
axm.bar(x, m.margen, color=[PALETTE["good"] if v >= 0 else PALETTE["bad"] for v in m.margen])
axm.axhline(0, color=PALETTE["ink"], lw=0.8)
axm.set_ylabel("Margen %")
axm.set_xticks(x, etq, rotation=45, ha="right")
axm.grid(axis="x", visible=False)

# Gráfico 2: saldo de caja
fig2, ax = plt.subplots(figsize=(7.6, 3.9))
ax.fill_between(x, m.caja / 1e6, color=PALETTE["primary"], alpha=0.15)
ax.plot(x, m.caja / 1e6, color=PALETTE["primary"], lw=2.6, marker="o")
bajos = m.utilidad < 0
ax.scatter(x[bajos.values], (m.caja / 1e6)[bajos], color=PALETTE["bad"], zorder=3, s=60, label="Mes con pérdida")
ax.set_xticks(x, etq, rotation=45, ha="right")
ax.set_ylabel("Millones COP")
ax.set_title("Saldo de caja acumulado")
if bajos.any():
    ax.legend(frameon=False)

# Gráfico 3: estructura de gastos
gc = df[df.tipo == "Gasto"].groupby("categoria")["monto"].sum().sort_values()
fig3, ax = plt.subplots(figsize=(7.6, 4.2))
cols = [PALETTE["accent"] if c in FIJOS else PALETTE["muted"] if c in EXTRAS else PALETTE["primary"] for c in gc.index]
ax.barh(gc.index, gc.values / 1e6, color=cols)
for i, v in enumerate(gc.values):
    ax.text(v / 1e6, i, f" {v / gc.sum() * 100:.0f}%", va="center", fontsize=9, color=PALETTE["ink"])
ax.set_xlabel("Millones COP (12 meses)")
ax.set_title("¿En qué se va el dinero?")
ax.grid(axis="y", visible=False)
ax.set_xlim(0, gc.max() / 1e6 * 1.15)

# Gráfico 4: ingresos por línea de negocio
li = df[df.tipo == "Ingreso"].groupby(["mes", "categoria"])["monto"].sum().unstack(fill_value=0) / 1e6
fig4, ax = plt.subplots(figsize=(7.6, 4.2))
ax.stackplot(x, li.T.values, labels=li.columns, colors=SERIES[: li.shape[1]], alpha=0.9)
ax.set_xticks(x, etq, rotation=45, ha="right")
ax.set_ylabel("Millones COP")
ax.set_title("Ingresos por línea de negocio")
ax.legend(frameon=False, loc="upper left", fontsize=8, ncol=2)
ax.grid(axis="x", visible=False)
ax.set_ylim(0, li.sum(axis=1).max() * 1.3)

# Tabla mensual
filas = []
for p, r in m.iterrows():
    kind = "bad" if r.margen < 5 else "warn" if r.margen < 12 else "good"
    filas.append([f"{MESES[p.month - 1]} {p.year}", money(r.ingresos), money(r.gastos), money(r.utilidad), tag(f"{r.margen:.1f}%", kind), money(r.caja)])
tabla = table_html(["Mes", "Ingresos", "Gastos", "Utilidad", "Margen", "Caja acumulada"], filas)

mejor, peor = m.utilidad.idxmax(), m.utilidad.idxmin()
render_dashboard(
    "tablero.html",
    "Panel de finanzas · Pastelería artesanal",
    "Nov 2025 – oct 2026 · Valores en COP · Datos de ejemplo",
    kpis=[
        ("Utilidad (12 meses)", money(m.utilidad.sum()), f"margen {m.utilidad.sum() / m.ingresos.sum() * 100:.1f}%", "up" if m.utilidad.sum() > 0 else "down"),
        ("Ingresos (12 meses)", money(m.ingresos.sum())),
        ("Caja actual", money(m.caja.iloc[-1]), f"inicio: {money(CAJA_INICIAL)}"),
        ("Punto de equilibrio mensual", money(equilibrio), f"vende {m.ingresos.mean() / equilibrio:.2f}x ese nivel en promedio"),
        ("Mejor / peor mes", f"{MESES[mejor.month - 1]} / {MESES[peor.month - 1]}", f"{money(m.utilidad[mejor])} / {money(m.utilidad[peor])}"),
    ],
    sections=[
        {"title": "Resultado y caja", "note": "Arriba: ingresos y gastos de cada mes. Abajo: margen de utilidad (rojo si hubo pérdida). A la derecha, el saldo de caja; un punto rojo marca un mes con pérdida.", "figs": [fig1, fig2]},
        {"title": "Estructura de ingresos y gastos", "note": "Naranja: gastos fijos. Azul: gastos que crecen con las ventas. Gris: gastos no recurrentes (equipos e impuestos).", "figs": [fig3, fig4]},
        {"title": "Resumen mensual", "note": "Margen en rojo por debajo de 5%, amarillo entre 5% y 12%, verde desde 12%.", "html": tabla},
    ],
)
print(m.round(1).to_string())
print("equilibrio:", round(equilibrio), "fijos prom:", round(fijos_m), "mc:", round(mc, 3))

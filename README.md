# Panel de finanzas para negocios pequeños

Convierte el registro de ingresos y gastos de un negocio (un Excel o CSV) en un panel que responde:
**¿gané o perdí cada mes?, ¿cuánta caja tengo?, ¿en qué se va el dinero? y ¿cuánto necesito vender
para no perder?**

## Qué incluye

- Utilidad, margen y saldo de caja mes a mes; los meses con pérdida se marcan en rojo.
- **Punto de equilibrio mensual:** ventas necesarias para cubrir los costos fijos.
- Estructura de gastos: fijos, variables y no recurrentes (equipos, impuestos).
- Ingresos por línea de negocio (mostrador, encargos, eventos, domicilios).
- Resumen mensual con semáforo de margen.

## Cómo calcula el punto de equilibrio

```
margen de contribución = 1 − (gastos variables ÷ ingresos)
punto de equilibrio    = costos fijos mensuales ÷ margen de contribución
```

Los costos fijos son arriendo, nómina, servicios, marketing y mantenimiento. Los gastos no
recurrentes (equipos, impuestos) no entran al cálculo.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `generate_data.py` | Crea `movimientos.csv` (datos inventados de una pastelería, nov 2025 – oct 2026) |
| `panel.py` | Calcula indicadores y genera `tablero.html` |
| `dashboard_kit.py` | Diseño del tablero |

## Uso

```bash
pip install -r requirements.txt
python generate_data.py
python panel.py
```

## Con datos reales

Usa un `movimientos.csv` con las columnas `fecha, tipo (Ingreso/Gasto), categoria, monto`. Ajusta
`CAJA_INICIAL` y las listas `FIJOS` y `EXTRAS` al inicio de `panel.py` según las categorías del negocio.

## Tecnologías

Python, pandas, matplotlib, HTML/CSS.

> Datos inventados con semilla fija.


## Qué busca (el problema)

Muchos negocios pequeños no saben si ganan, cuánta caja tienen ni cuánto deben vender para no perder.

## Cómo se cumple

Convierte los movimientos en utilidad, caja, punto de equilibrio y estructura de gastos mes a mes.

## Cómo ofrecerlo como servicio

- **Qué entrego:** Panel financiero a la medida a partir de tus movimientos (Excel o extractos).
- **A quién:** Pastelerías, talleres, consultorios y comercios con contabilidad informal.
- **Precio de referencia (ajustar):** Panel inicial: 400.000–1.000.000 COP. Cierre mensual: 150.000–350.000 COP.
- **Frase para empezar:** «Te digo cuánto necesitas vender al mes para ganar plata y dónde se te va el gasto.»
- **Flujo:** 1) reunión corta y datos del cliente → 2) prototipo con sus datos → 3) ajustes → 4) entrega y capacitación.

> Datos del repositorio inventados; ejecutar los scripts para reproducir el tablero.

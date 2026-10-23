"""
Dashboard final de WaferPi (Unidad 4).

Genera dashboard/waferpi_dashboard.html: una sola página con
  - título con el hallazgo principal,
  - filtro por conjunto (Todos / Training / Test),
  - tarjetas KPI,
  - % promedio de dies fallados por patrón,
  - obleas con falla por patrón,
  - mapas de oblea interactivos por patrón.

Uso (desde la raíz del repositorio, con el entorno .venv activo):
    python dashboard/construir_dashboard.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RUTA_PKL = RAIZ / "data" / "LSWMD.pkl"
RUTA_CSV = RAIZ / "data" / "processed" / "obleas_etiquetadas.csv"
SALIDA = RAIZ / "dashboard" / "waferpi_dashboard.html"

PATRONES = ["Center", "Donut", "Edge-Loc", "Edge-Ring", "Loc", "Near-full", "Random", "Scratch"]
BORDE = ["Edge-Ring", "Edge-Loc"]          # fallas en la orilla de la oblea
SEVEROS = ["Near-full", "Random"]          # los únicos que se separan por % de fallo


# ---------------------------------------------------------------------------
# 1. Resumen por conjunto (tabla por oblea exportada por el notebook)
# ---------------------------------------------------------------------------
tabla = pd.read_csv(RUTA_CSV)

def resumir(df):
    con_patron = df[df["patron"] != "none"]
    conteo = con_patron["patron"].value_counts()
    promedio = con_patron.groupby("patron")["pct_fallados"].mean()
    return {
        "etiquetadas": int(len(df)),
        "con_patron": int(len(con_patron)),
        "pct_sin_patron": round(100 * (df["patron"] == "none").mean(), 1),
        "pct_borde": round(100 * conteo[BORDE].sum() / len(con_patron), 1),
        "conteo": {p: int(conteo.get(p, 0)) for p in PATRONES},
        "promedio": {p: round(float(promedio.get(p, 0)), 1) for p in PATRONES},
    }

resumen = {
    "Todos": resumir(tabla),
    "Training": resumir(tabla[tabla["conjunto"] == "Training"]),
    "Test": resumir(tabla[tabla["conjunto"] == "Test"]),
}

# ---------------------------------------------------------------------------
# 2. Mapas de ejemplo: 3 obleas típicas por patrón (mismo criterio del Avance 3)
# ---------------------------------------------------------------------------
print("Leyendo LSWMD.pkl (~1 minuto)...")
crudo = pd.read_pickle(RUTA_PKL)

def desenvolver(valor):
    arr = np.asarray(valor)
    return str(arr.ravel()[0]) if arr.size else None

crudo["patron"] = crudo["failureType"].apply(desenvolver)
crudo = crudo[crudo["patron"].isin(PATRONES)].copy()
crudo["pct"] = crudo["waferMap"].apply(lambda m: 100 * (np.asarray(m) == 2).sum() / (np.asarray(m) != 0).sum())

mapas = {}
for p in PATRONES:
    c = crudo[(crudo["patron"] == p) & crudo["dieSize"].between(500, 1500)]
    q1, q3 = c["pct"].quantile([0.25, 0.75])
    elegidas = c[c["pct"].between(q1, q3)].sample(3, random_state=42)
    mapas[p] = [{
        "lote": fila.lotName,
        "indice": int(fila.waferIndex),
        "dies": int(fila.dieSize),
        "pct": round(float(fila.pct), 1),
        "mapa": np.asarray(fila.waferMap).astype(int).tolist(),
    } for fila in elegidas.itertuples()]

# ---------------------------------------------------------------------------
# 3. Página HTML (Plotly.js dibuja las gráficas con los datos de arriba)
# ---------------------------------------------------------------------------
plantilla = (RAIZ / "dashboard" / "plantilla.html").read_text(encoding="utf-8")
datos = json.dumps({"resumen": resumen, "mapas": mapas, "patrones": PATRONES,
                    "borde": BORDE, "severos": SEVEROS}, separators=(",", ":"))
SALIDA.write_text(plantilla.replace("__DATOS__", datos), encoding="utf-8")
print("Dashboard generado:", SALIDA.relative_to(RAIZ))

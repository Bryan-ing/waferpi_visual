# Datos

## Dataset original (no incluido en el repositorio)

| | |
|---|---|
| **Nombre** | WM-811K (LSWMD) |
| **Archivo** | `LSWMD.pkl` (~2.1 GB) |
| **Descarga** | Kaggle — https://www.kaggle.com/datasets/qingyi/wm811k-wafer-map |
| **Artículo original** | Wu, Jang y Chen (2015), *IEEE Transactions on Semiconductor Manufacturing, 28*(1), 1–12. https://doi.org/10.1109/TSM.2014.2364237 |
| **Contenido** | 811,457 mapas de oblea de 46,293 lotes; 172,950 con patrón de falla etiquetado |

No se sube a GitHub porque supera el límite de 100 MB por archivo.

**Pasos:**
1. Descarga el dataset desde Kaggle (requiere cuenta gratuita).
2. Descomprime el `.zip` (clic derecho → *Extraer todo* en Windows).
3. Copia `LSWMD.pkl` a esta carpeta: `data/LSWMD.pkl`.

> El archivo se guardó con una versión antigua de pandas. Para abrirlo se necesitan **pandas 1.5.3 y numpy < 2** (ya fijados en `requirements.txt`). Con pandas 2.x aparece el error `No module named 'pandas.indexes'`.

## Datos procesados (`processed/`)

| Archivo | Cómo se genera | Uso |
|---|---|---|
| `obleas_etiquetadas.csv` | Sección 5 del notebook | Fuente de datos del dashboard de Tableau |

Una fila por oblea etiquetada (172,950 filas). Columnas: `id_oblea`, `lote`, `indice_oblea`, `patron`, `tiene_patron`, `conjunto`, `dies_totales`, `dies_fallados`, `pct_fallados`.

### Transformaciones aplicadas al original
1. `failureType` y `trianTestLabel` venían como arreglos anidados (`array([['Center']])`) → se convirtieron a texto (`patron`, `conjunto`); los vacíos quedan como sin etiqueta.
2. Del `waferMap` (0 = fuera de la oblea, 1 = die bueno, 2 = die fallado) se calcularon `dies_totales` (≠ 0) y `dies_fallados` (= 2).
3. `pct_fallados = 100 · dies_fallados / dies_totales`.
4. Se conservaron solo las obleas con patrón etiquetado (incluye `none`).
5. Verificación: `dieSize` coincide exactamente con `dies_totales` en las 811,457 obleas.

No hubo ediciones manuales: todo está en el notebook.

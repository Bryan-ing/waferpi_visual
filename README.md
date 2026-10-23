# WaferPi · Visualización de defectos en obleas semiconductoras (WM-811K)

Proyecto de la materia **Visualización de Datos** — Maestría Profesionalizante en Inteligencia Artificial, Instituto Tecnológico de Aguascalientes (TecNM).
**Autor:** Ing. Bryan Guadalupe De la paz Coronado · **Profesor:** Dr. Ricardo Emmanuel Reyes Acosta

> **Pregunta analítica:** ¿es posible distinguir visualmente el tipo de patrón de falla de una oblea a partir de la distribución espacial de sus dies fallados?

Este repositorio es la base visual del proyecto de tesis **WaferPi** (clasificación de patrones de falla en obleas y despliegue en Raspberry Pi 5).

---

## Resultados

| Tipo | Visualización | Archivo / enlace |
|---|---|---|
| Estática (matplotlib) | Número de dies por oblea vs % de dies fallados | [`figures/final_estatica_diesize_vs_fallo.png`](figures/final_estatica_diesize_vs_fallo.png) |
| Interactiva (Plotly) | Mapas de oblea por patrón (menú, hover, zoom) | [Ver en línea](https://bryan-ing.github.io/waferpi_visual/figures/final_interactivo_mapas_oblea.html) · [`figures/final_interactivo_mapas_oblea.html`](figures/final_interactivo_mapas_oblea.html) |
| BI (Tableau Public) | Dashboard: KPIs, obleas y % de fallo por patrón, filtros | [Ver en Tableau Public](https://public.tableau.com/app/profile/bryan.de.la.paz/viz/WaferPi-PatronesdefallaWM-811K/Dashboard1) · [`Dashboard Tableau/wafer_dashboard.twbx`](Dashboard%20Tableau/wafer_dashboard.twbx) |
| **Dashboard final (Unidad 4)** | Hallazgo principal, KPIs, % de fallo y obleas por patrón, mapas interactivos, filtro por conjunto | [Ver en línea](https://bryan-ing.github.io/waferpi_visual/dashboard/waferpi_dashboard.html) · [`dashboard/`](dashboard/) |
| EDA (Avance 2) | Univariada, bivariada, multivariada y condicional | [`figures/`](figures/) (`avance2_*.png`) |

Las capturas y la explicación de cada visualización están en [Documentación de las visualizaciones](#documentación-de-las-visualizaciones).

---

## Documentación de las visualizaciones

El flujo completo está en el notebook, en este orden: **0. Configuración → 1. Carga → 2. Limpieza → 3. EDA → 4. Visualizaciones finales → 5. Exportación para BI → 6. Dashboard de Tableau**. Cada sección inicia con una celda markdown que explica qué se hace y por qué, y cada figura tiene debajo su interpretación.

### 1. EDA del Avance 2 · matplotlib (notebook, sección 3)

| Figura | Qué muestra | Hallazgo |
|---|---|---|
| ![](figures/avance2_univariada.png) | **Univariada:** obleas por patrón de falla | `none` es el 85.2% de las obleas etiquetadas: desbalance de clases fuerte |
| ![](figures/avance2_bivariada.png) | **Bivariada:** dieSize vs % de dies fallados | Relación negativa débil (r = −0.22); sobretrazado y escala mal aprovechada → se rediseña |
| ![](figures/avance2_multivariada.png) | **Multivariada:** mapa de una oblea (X, Y, estado del die) | La falla Edge-Ring forma un anillo en el borde; un solo mapa no permite comparar → se rediseña |
| ![](figures/avance2_condicional.png) | **Condicional:** % de dies fallados por patrón (boxplot) | Solo Near-full y Random se separan; los demás se traslapan entre 9% y 26% |

### 2. Visualización estática final · matplotlib (notebook, sección 4.1)

![Estática final](figures/final_estatica_diesize_vs_fallo.png)

- **Mejoras frente al Avance 2:** hexbin en lugar de 172,950 puntos encimados, eje X logarítmico, mediana y rango intercuartil por rango de dieSize, anotaciones calculadas con los datos y un título que enuncia el hallazgo.
- **Cómo leerla:** un hexágono más oscuro agrupa más obleas. La línea naranja es la mediana y la franja es el 50% central.
- **Hallazgo:** el % de fallo baja conforme aumenta el número de dies por oblea (Spearman ρ = −0.57). Hay un repunte entre 2,000 y 5,000 dies que se asocia al patrón Edge-Ring.

### 3. Visualización interactiva · Plotly (notebook, sección 4.2)

[Abrir la visualización en línea](https://bryan-ing.github.io/waferpi_visual/figures/final_interactivo_mapas_oblea.html)

| Vista inicial (Edge-Ring) | Hover sobre un die |
|---|---|
| ![](docs/capturas/interactivo_vista_inicial.png) | ![](docs/capturas/interactivo_hover.png) |
| **Menú de patrones** | **Scratch con "Solo dies fallados"** |
| ![](docs/capturas/interactivo_menu.png) | ![](docs/capturas/interactivo_scratch_solo_fallados.png) |

- **Interacción:**
  - **Menú desplegable:** elige entre los 8 patrones y `none`; cada uno muestra 3 obleas reales.
  - **Botones:** "Todos los dies" / "Solo dies fallados".
  - **Hover:** muestra lote, oblea, posición, estado del die y % de fallo.
  - **Zoom y paneo.**
- **Selección de ejemplos:** obleas con 500–1,500 dies y % de fallo dentro del rango intercuartil de su patrón, elegidas con `random_state=42`.
- **Hallazgo:** la forma de la falla se repite dentro de cada patrón y cambia entre patrones. Sí es posible distinguir el patrón visualmente por la distribución espacial de los dies fallados.

### 4. Dashboard de BI · Tableau Public (notebook, secciones 5 y 6)

[Abrir el dashboard en Tableau Public](https://public.tableau.com/app/profile/bryan.de.la.paz/viz/WaferPi-PatronesdefallaWM-811K/Dashboard1)

![Dashboard de Tableau](docs/capturas/tableau_dashboard.png)

- **Datos:** `data/processed/obleas_etiquetadas.csv`, exportado por el notebook. Va guardado como extracción dentro de `Dashboard Tableau/wafer_dashboard.twbx`.
- **Componentes:**
  - 3 KPI: obleas etiquetadas, obleas con patrón (campo calculado) y % promedio de dies fallados.
  - Barras de obleas por patrón, con color que separa `none` del resto.
  - Barras de % de fallo por patrón.
- **Interacción:**
  - Filtros por patrón y por conjunto (Training/Test), aplicados a todas las hojas.
  - Clic en una barra de "Obleas por patrón" filtra el resto del dashboard.
  - Tooltip personalizado.
- **Hallazgo:** en una sola vista se ve el desbalance de clases y que solo Near-full (87.7%) y Random (48.1%) se distinguen por el % de fallo. Los demás patrones necesitan el mapa espacial.

---

## Estructura del repositorio

```
waferpi_visual/
├── README.md                     ← este archivo
├── requirements.txt              ← versiones exactas de las librerías
├── notebooks/
│   └── waferpi_avance3.ipynb     ← TODO el flujo: carga → limpieza → EDA → visualizaciones finales → BI
├── data/
│   ├── README.md                 ← fuente del dataset y transformaciones aplicadas
│   ├── LSWMD.pkl                 ← dataset original (NO se sube; se descarga de Kaggle)
│   └── processed/
│       └── obleas_etiquetadas.csv  ← tabla por oblea para Tableau (generada por el notebook)
├── figures/                      ← figuras generadas por el notebook
├── dashboard/
│   ├── construir_dashboard.py    ← genera el dashboard final desde los datos
│   ├── plantilla.html            ← diseño de la página
│   └── waferpi_dashboard.html    ← dashboard final (Python + Plotly)
├── Dashboard Tableau/
│   └── wafer_dashboard.twbx    ← dashboard de Tableau empaquetado (incluye extracción de datos)
└── docs/
    └── capturas/                 ← capturas de las visualizaciones interactivas y del dashboard
```

---

## Cómo reproducir el proyecto

### 1. Requisitos
- **Python 3.11** (o 3.10). pandas 1.5.3 no tiene versión para Python 3.12 o superior.
  En Windows se descarga de https://www.python.org/downloads/ (marca *Add Python to PATH*).
- ~4 GB de RAM libres y ~3 GB de disco (el dataset pesa 2.1 GB).

### 2. Clonar el repositorio y crear el entorno
```bash
git clone https://github.com/Bryan-ing/waferpi_visual.git
cd waferpi_visual
py -3.11 -m venv .venv            # Windows   (Linux/Mac: python3.11 -m venv .venv)
.venv\Scripts\activate            # Windows   (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

### 3. Descargar el dataset
Descarga **WM-811K** de Kaggle (https://www.kaggle.com/datasets/qingyi/wm811k-wafer-map), descomprime y copia `LSWMD.pkl` en `data/`. Detalles en [`data/README.md`](data/README.md).

### 4. Ejecutar el notebook
```bash
jupyter notebook notebooks/waferpi_avance3.ipynb
```
Menú **Run → Run All Cells**. Tarda ~3 minutos (la carga del `.pkl` ocupa ~1 minuto). Al terminar, `figures/` y `data/processed/` quedan regenerados.

### 5. Generar el dashboard final
```bash
python dashboard/construir_dashboard.py
```
Requiere haber ejecutado antes el notebook (usa `data/processed/obleas_etiquetadas.csv`).

> **Error `No module named 'pandas.indexes'`:** estás usando pandas 2.x. Verifica que activaste el entorno `.venv` con Python 3.11 e instalaste `requirements.txt`.

---

## Decisiones de reproducibilidad
- **Datos originales intactos:** el `.pkl` solo se lee; todo lo derivado se guarda en `data/processed/`.
- **Sin pasos manuales:** limpieza, cálculos, figuras y exportación a Tableau están en el notebook.
- **Rutas relativas:** el notebook funciona en cualquier computadora sin editar rutas.
- **Selección aleatoria con semilla** (`random_state=42`) para los mapas de ejemplo.
- **Versiones fijas** en `requirements.txt`.
- **Cifras calculadas, no escritas:** todas las anotaciones de las figuras salen de los datos.

## Fuentes
- Wu, M.-J., Jang, J.-S. R., & Chen, J.-L. (2015). Wafer map failure pattern recognition and similarity ranking for large-scale data sets. *IEEE Transactions on Semiconductor Manufacturing, 28*(1), 1–12. https://doi.org/10.1109/TSM.2014.2364237
- Dataset en Kaggle: https://www.kaggle.com/datasets/qingyi/wm811k-wafer-map

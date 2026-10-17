# Guía paso a paso: dashboard en Tableau Public

**Objetivo:** construir un dashboard con **tarjetas KPI**, **gráfica de obleas por patrón**, **% de fallo por patrón**, **filtros interactivos** y **tooltip personalizado**, y publicarlo con un enlace público.

**Tiempo estimado:** 30–45 minutos.
**Archivo de datos:** `data/processed/obleas_etiquetadas.csv` (172,950 filas, una por oblea).

---

## 1. Instalar Tableau Public
1. Entra a **public.tableau.com** → *Create* → **Download the app** (Tableau Public Desktop, gratis).
2. Crea tu cuenta gratuita con tu correo (te la va a pedir para publicar).
3. Instala y abre la aplicación.

## 2. Conectar los datos
1. En el panel izquierdo, *Connect* → **Text file** → elige `obleas_etiquetadas.csv`.
2. Revisa los íconos de tipo arriba de cada columna:
   - `pct_fallados`, `dies_totales`, `dies_fallados`, `indice_oblea` deben tener **#** (número).
   - Si `pct_fallados` aparece con **Abc** (texto), clic en el ícono → **Número (decimal)**.
   - Si los valores salen raros (ej. 523 en vez de 5.23), es por la configuración regional: menú **File → Workbook Locale → English (United States)**.
3. Abajo a la izquierda, clic en **Sheet 1** para ir a la primera hoja.

> Tableau separa los campos en **Dimensiones** (texto para agrupar: `patron`, `conjunto`, `tiene_patron`) y **Medidas** (números que se agregan: `pct_fallados`, `dies_fallados`). Es lo mismo que vimos en el Tema 3.3.4.

## 3. Hojas de KPI (3 tarjetas)

**Hoja "KPI · Obleas"**
1. Arrastra **`obleas_etiquetadas.csv (Count)`** (está al final de la lista de campos) a **Text** en la tarjeta *Marks*.
2. Formato grande: clic en *Text* → **…** → fuente tamaño 28, negrita.
3. Renombra la hoja (doble clic en la pestaña): `KPI · Obleas`.
4. Debe decir **172,950**.

**Hoja "KPI · Con patrón"**
1. Menú **Analysis → Create Calculated Field**, nombre `Obleas con patrón`, fórmula:
   ```
   SUM(IF [tiene_patron] = "Con patrón" THEN 1 ELSE 0 END)
   ```
2. Arrástralo a **Text**. Debe decir **25,519**.

**Hoja "KPI · % fallo"**
1. Arrastra `pct_fallados` a **Text**, clic derecho → **Measure → Average**.
2. Clic derecho → *Format* → Números → 1 decimal y sufijo `%`. Debe decir **11.8%**.

## 4. Hoja "Obleas por patrón" (barras)
1. `patron` a **Rows**, `obleas_etiquetadas.csv (Count)` a **Columns**.
2. Botón de ordenar descendente en la barra de herramientas.
3. Arrastra `tiene_patron` a **Color** (resalta que `none` domina: desbalance de clases).
4. Arrastra el conteo a **Label** para ver el número en cada barra.

Valores esperados: none 147,431 · Edge-Ring 9,680 · Edge-Loc 5,189 · Center 4,294 · Loc 3,593 · Scratch 1,193 · Random 866 · Donut 555 · Near-full 149.

## 5. Hoja "% de fallo por patrón" (barras)
1. `patron` a **Rows**, `pct_fallados` a **Columns** → clic derecho → **Measure → Average**.
2. Orden descendente. Valores esperados: Near-full ≈ 87.7%, Random ≈ 48.1%, Donut ≈ 27.7% … Scratch ≈ 10.1%.

## 6. Tooltip personalizado (en la hoja "Obleas por patrón")
1. Arrastra `pct_fallados` (como **Average**) y `dies_totales` (como **Average**) a **Tooltip**.
2. Clic en **Tooltip** y reemplaza el texto por:
   ```
   Patrón: <patron>
   Obleas: <CNT(obleas_etiquetadas.csv)>
   % promedio de dies fallados: <AVG(pct_fallados)>%
   Dies promedio por oblea: <AVG(dies_totales)>
   ```
   (usa el botón **Insert** para meter los campos en lugar de escribirlos).

## 7. Filtros interactivos
1. En la hoja de barras, arrastra `conjunto` a **Filters** → selecciona todo → OK.
2. Clic derecho en el filtro → **Show Filter** (aparece a la derecha).
3. Clic derecho en el filtro → **Apply to Worksheets → All Using This Data Source** (así filtra también los KPI).
4. Repite con `patron` (útil para quitar `none` y ver solo los 8 patrones).

## 8. Armar el dashboard
1. Abajo, ícono **New Dashboard**. En *Size* elige **Automatic** (o 1200 × 800).
2. Arrastra las 3 hojas KPI en una fila arriba (usa un contenedor **Horizontal** de *Objects*).
3. Abajo, las dos gráficas de barras lado a lado.
4. Arrastra un objeto **Text** arriba con el título: `WaferPi · Patrones de falla en obleas (WM-811K)` y una línea con la fuente: `Fuente: WM-811K (Wu, Jang y Chen, 2015)`.
5. **Acción de filtro:** selecciona la gráfica "Obleas por patrón" en el dashboard → ícono de embudo (**Use as Filter**). Ahora, al dar clic en una barra, se filtran los KPI y la otra gráfica.

## 9. Publicar
1. **File → Save to Tableau Public As…** → nombre: `WaferPi - Patrones de falla WM-811K`.
2. Inicia sesión; se abre el navegador con tu viz publicada.
3. Copia el **enlace** de la barra de direcciones y toma una **captura de pantalla** del dashboard.
4. Pega el enlace en el `README.md` del repo (sección *Resultados*) y en el PDF.

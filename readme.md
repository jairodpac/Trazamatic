# Proyecto ETL Trazamatic

Sistema completo de ETL y analíticos para la gestión y análisis de datos de producción textil de Trazamatic.

## 🎯 Características

- **ETL Completo**: Extracción, transformación y carga de 7 datasets
- **15+ KPIs**: Indicadores de negocio en 4 áreas (Producción, Financiero, Clientes, Inventario)
- **3 Dashboards Interactivos**: Visualizaciones con Streamlit y Plotly
- **Tablas Analíticas**: 5 tablas agregadas para análisis rápido

## 📊 Dashboards Disponibles

### 1. Dashboard Ejecutivo
Vista general con KPIs principales y tendencias clave.

**Ejecutar:**
```bash
streamlit run src/visualization/dashboard_ejecutivo.py
```

**Incluye:**
- 4 KPIs principales (Ingresos, Completitud, Órdenes en proceso, Clientes activos)
- Tendencia de ingresos mensuales
- Top 10 productos por ingresos
- Distribución de estados de órdenes
- Clientes por ciudad
- Últimas 10 órdenes

### 2. Dashboard de Producción
Análisis de productividad y desempeño operacional.

**Ejecutar:**
```bash
streamlit run src/visualization/dashboard_produccion.py
```

**Incluye:**
- Productividad por empleado
- Tasa de completitud vs volumen
- Timeline de estados de órdenes
- Distribución por día de la semana
- Detalle de productividad

### 3. Dashboard Financiero
Análisis de ingresos, costos y rentabilidad.

**Ejecutar:**
```bash
streamlit run src/visualization/dashboard_financiero.py
```

**Incluye:**
- Top 15 productos por ingresos
- Top 15 clientes por ingresos
- Evolución de ingresos mensuales
- Curva de concentración (Pareto)
- Análisis ticket promedio vs volumen

## 🚀 Instalación

1. **Clonar el repositorio** (si aplica)

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar el proceso ETL:**
```bash
python src/etl.py
```

Esto generará:
- Datos limpios en `data/processed/`
- Tablas analíticas en `data/analytics/`

## 📁 Estructura del Proyecto

```
Trazamatic/
├── data/
│   ├── raw/                    # Datos originales (CSV)
│   ├── processed/              # Datos limpios
│   └── analytics/              # Tablas analíticas agregadas
├── src/
│   ├── etl/                    # Módulos ETL
│   │   ├── extract.py          # Extracción de datos
│   │   ├── transform.py        # Limpieza y transformación
│   │   └── load.py             # Carga y agregación
│   ├── analytics/              # Cálculo de KPIs
│   │   └── kpis.py             # 15+ KPIs de negocio
│   ├── visualization/          # Dashboards
│   │   ├── app.py              # Aplicación principal
│   │   ├── dashboard_ejecutivo.py
│   │   ├── dashboard_produccion.py
│   │   └── dashboard_financiero.py
│   └── etl.py                  # Script principal ETL
├── notebooks/
│   └── clientes.ipynb          # Análisis exploratorio
├── config/
├── requirements.txt
└── readme.md
```

## 📊 KPIs Implementados

### Producción (5 KPIs)
- Tasa de Completitud de Órdenes (Objetivo: >85%)
- Tiempo Promedio de Producción (Objetivo: <15 días)
- Productividad por Empleado (Objetivo: >5 órdenes/mes)
- Eficiencia de Uso de Materiales (Objetivo: 70-85%)
- Órdenes en Proceso (Monitoreo)

### Financiero (4 KPIs)
- Ingresos Totales
- Ingresos del Mes
- Ticket Promedio (Objetivo: >$5,000)
- Concentración Top 10 Clientes (Objetivo: <50%)

### Clientes (4 KPIs)
- Clientes Activos (últimos 90 días)
- Tasa de Retención (Objetivo: >60%)
- Frecuencia de Compra (Objetivo: >3 órdenes/año)
- Distribución Geográfica

### Inventario (3 KPIs)
- Rotación de Materiales (Objetivo: >4 veces/año)
- Stock Crítico (Objetivo: 0 materiales)
- Top 10 Materiales Más Usados

## 🔄 Actualización de Datos

Para actualizar los datos y recalcular las tablas analíticas:

```bash
python src/etl.py
```

Los dashboards se actualizarán automáticamente al recargar.

## 🛠️ Tecnologías Utilizadas

- **Python 3.13**
- **Pandas** - Manipulación de datos
- **Streamlit** - Framework de dashboards
- **Plotly** - Gráficos interactivos
- **NumPy** - Cálculos numéricos

## 📝 Uso

### 1. Ejecutar ETL
```bash
python src/etl.py
```

### 2. Ver Dashboard Ejecutivo
```bash
streamlit run src/visualization/dashboard_ejecutivo.py
```

### 3. Ver Dashboard de Producción
```bash
streamlit run src/visualization/dashboard_produccion.py
```

### 4. Ver Dashboard Financiero
```bash
streamlit run src/visualization/dashboard_financiero.py
```

### 5. Ver Aplicación Principal
```bash
streamlit run src/visualization/app.py
```

## 📈 Datos Procesados

El sistema procesa 7 datasets:
- **clientes.csv** (1,500 registros)
- **ordenes_produccion.csv** (1,500 registros)
- **productos.csv** (1,500 registros)
- **materiales.csv** (1,500 registros)
- **empleados.csv** (1,500 registros)
- **detalles_orden.csv** (1,500 registros)
- **uso_materiales.csv** (1,500 registros)

Y genera 5 tablas analíticas:
- **ordenes_completas.csv** - Órdenes con información completa
- **ventas_por_producto.csv** - Ventas agregadas por producto
- **metricas_por_cliente.csv** - Métricas por cliente
- **productividad_empleados.csv** - Productividad por empleado
- **uso_materiales_agregado.csv** - Uso de materiales agregado

## 📄 Licencia

Consulta el archivo [licence.md](licence.md) para más información.

## 👤 Autor

Trazamatic - Equipo de Analíticos
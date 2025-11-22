"""
Dashboard Ejecutivo - Trazamatic
Vista general con KPIs principales y visualizaciones clave.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from analytics.kpis import KPICalculator


# Configuración de la página
st.set_page_config(
    page_title="Dashboard Ejecutivo - Trazamatic",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .metric-positive {
        color: #10b981;
    }
    .metric-negative {
        color: #ef4444;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_kpis():
    """Carga y cachea los KPIs."""
    calculator = KPICalculator()
    return calculator.calcular_todos_kpis()


@st.cache_data(ttl=3600)
def load_analytics_data():
    """Carga los datos analíticos."""
    return {
        'ordenes': pd.read_csv('data/analytics/ordenes_completas.csv'),
        'ventas_producto': pd.read_csv('data/analytics/ventas_por_producto.csv'),
        'metricas_cliente': pd.read_csv('data/analytics/metricas_por_cliente.csv'),
        'productividad': pd.read_csv('data/analytics/productividad_empleados.csv')
    }


def render_kpi_card(kpi_data, col):
    """Renderiza una tarjeta de KPI."""
    with col:
        valor = kpi_data['valor']
        unidad = kpi_data.get('unidad', '')
        nombre = kpi_data['nombre']
        
        # Determinar si cumple objetivo
        cumple = kpi_data.get('cumple_objetivo', None)
        if cumple is not None:
            icon = "✅" if cumple else "⚠️"
        else:
            icon = "📊"
        
        # Formatear valor
        if unidad == '$':
            valor_str = f"${valor:,.2f}"
        elif unidad == '%':
            valor_str = f"{valor:.1f}%"
        else:
            valor_str = f"{valor:,.0f}"
        
        st.metric(
            label=f"{icon} {nombre}",
            value=valor_str,
            delta=f"Objetivo: {kpi_data.get('objetivo', 'N/A')}" if 'objetivo' in kpi_data else None
        )


def plot_ingresos_tendencia(data):
    """Gráfico de tendencia de ingresos."""
    # Agrupar por mes
    df = data['metricas_cliente'].copy()
    df['ultima_orden'] = pd.to_datetime(df['ultima_orden'])
    df['mes'] = df['ultima_orden'].dt.to_period('M').astype(str)
    
    ingresos_mes = df.groupby('mes')['ingresos_totales'].sum().reset_index()
    
    fig = px.line(
        ingresos_mes,
        x='mes',
        y='ingresos_totales',
        title='📈 Tendencia de Ingresos por Mes',
        labels={'mes': 'Mes', 'ingresos_totales': 'Ingresos ($)'},
        markers=True
    )
    
    fig.update_traces(
        line_color='#667eea',
        line_width=3,
        marker=dict(size=8)
    )
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def plot_top_productos(data):
    """Gráfico de top productos."""
    top_10 = data['ventas_producto'].nlargest(10, 'ingresos_totales')
    
    fig = px.bar(
        top_10,
        x='ingresos_totales',
        y='nombre_producto',
        orientation='h',
        title='🏆 Top 10 Productos por Ingresos',
        labels={'ingresos_totales': 'Ingresos ($)', 'nombre_producto': 'Producto'},
        color='ingresos_totales',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def plot_distribucion_estados(data):
    """Gráfico de distribución de estados de órdenes."""
    estados = data['ordenes']['estado'].value_counts()
    
    colors = {
        'Completado': '#10b981',
        'En Proceso': '#f59e0b',
        'Pendiente': '#6b7280',
        'Cancelado': '#ef4444'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=estados.index,
        values=estados.values,
        hole=0.4,
        marker=dict(colors=[colors.get(e, '#6b7280') for e in estados.index])
    )])
    
    fig.update_layout(
        title='📊 Distribución de Estados de Órdenes',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def plot_clientes_por_ciudad(data):
    """Gráfico de clientes por ciudad."""
    ciudad_counts = data['metricas_cliente']['ciudad'].value_counts().head(10)
    
    fig = px.bar(
        x=ciudad_counts.values,
        y=ciudad_counts.index,
        orientation='h',
        title='🗺️ Top 10 Ciudades por Número de Clientes',
        labels={'x': 'Número de Clientes', 'y': 'Ciudad'},
        color=ciudad_counts.values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def main():
    """Función principal del dashboard."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Dashboard Ejecutivo - Trazamatic</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Cargar datos
    with st.spinner('Cargando datos...'):
        kpis = load_kpis()
        data = load_analytics_data()
    
    # SECCIÓN 1: KPIs PRINCIPALES
    st.subheader("🎯 KPIs Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    render_kpi_card(kpis['financiero']['ingresos_mes'], col1)
    render_kpi_card(kpis['produccion']['tasa_completitud'], col2)
    render_kpi_card(kpis['produccion']['ordenes_en_proceso'], col3)
    render_kpi_card(kpis['clientes']['activos_90dias'], col4)
    
    st.markdown("---")
    
    # SECCIÓN 2: VISUALIZACIONES PRINCIPALES
    st.subheader("📈 Análisis de Tendencias")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_ingresos_tendencia(data), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_distribucion_estados(data), use_container_width=True)
    
    st.markdown("---")
    
    # SECCIÓN 3: TOP PRODUCTOS Y CLIENTES
    st.subheader("🏆 Rankings y Distribución")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_top_productos(data), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_clientes_por_ciudad(data), use_container_width=True)
    
    st.markdown("---")
    
    # SECCIÓN 4: TABLA DE ÚLTIMAS ÓRDENES
    st.subheader("📋 Últimas Órdenes")
    
    ultimas_ordenes = data['ordenes'].sort_values('fecha_orden', ascending=False).head(10)
    
    # Seleccionar columnas relevantes
    columnas_mostrar = ['id_orden', 'nombre_empresa', 'ciudad', 'fecha_orden', 
                       'estado', 'nombre_empleado']
    
    # Filtrar columnas que existen
    columnas_disponibles = [col for col in columnas_mostrar if col in ultimas_ordenes.columns]
    
    st.dataframe(
        ultimas_ordenes[columnas_disponibles],
        use_container_width=True,
        hide_index=True
    )
    
    # SIDEBAR: KPIs ADICIONALES
    with st.sidebar:
        st.header("📊 KPIs Adicionales")
        
        st.markdown("### 💰 Financiero")
        st.metric("Ticket Promedio", f"${kpis['financiero']['ticket_promedio']['valor']:,.2f}")
        st.metric("Concentración Top 10", f"{kpis['financiero']['concentracion_top10']['valor']:.1f}%")
        
        st.markdown("### 👥 Clientes")
        st.metric("Tasa de Retención", f"{kpis['clientes']['tasa_retencion']['valor']:.1f}%")
        st.metric("Frecuencia de Compra", f"{kpis['clientes']['frecuencia_compra']['valor']:.1f}")
        
        st.markdown("### 🏭 Producción")
        st.metric("Productividad/Empleado", f"{kpis['produccion']['productividad_empleado']['valor']:.1f}")
        st.metric("Eficiencia Materiales", f"{kpis['produccion']['eficiencia_materiales']['valor']:.1f}%")
        
        st.markdown("---")
        st.caption("Última actualización: Hoy")


if __name__ == "__main__":
    main()

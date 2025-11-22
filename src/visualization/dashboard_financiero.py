"""
Dashboard Financiero - Trazamatic
Análisis de ingresos, costos y rentabilidad.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from analytics.kpis import KPICalculator


st.set_page_config(
    page_title="Dashboard Financiero - Trazamatic",
    page_icon="💰",
    layout="wide"
)


@st.cache_data(ttl=3600)
def load_data():
    """Carga datos financieros."""
    calculator = KPICalculator()
    kpis = calculator.calcular_todos_kpis()
    
    data = {
        'ventas_producto': pd.read_csv('data/analytics/ventas_por_producto.csv'),
        'metricas_cliente': pd.read_csv('data/analytics/metricas_por_cliente.csv')
    }
    
    # Convertir fechas
    data['metricas_cliente']['ultima_orden'] = pd.to_datetime(
        data['metricas_cliente']['ultima_orden']
    )
    
    return kpis, data


def plot_ingresos_por_producto(data):
    """Gráfico de ingresos por producto."""
    top_15 = data['ventas_producto'].nlargest(15, 'ingresos_totales')
    
    fig = px.bar(
        top_15,
        x='ingresos_totales',
        y='nombre_producto',
        orientation='h',
        title='💰 Top 15 Productos por Ingresos',
        labels={'ingresos_totales': 'Ingresos ($)', 'nombre_producto': 'Producto'},
        color='ingresos_totales',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(height=500, showlegend=False)
    
    return fig


def plot_ticket_vs_volumen(data):
    """Gráfico de ticket promedio vs volumen."""
    top_20 = data['ventas_producto'].nlargest(20, 'ingresos_totales')
    
    fig = px.scatter(
        top_20,
        x='num_ordenes',
        y='ticket_promedio',
        size='ingresos_totales',
        color='ingresos_totales',
        hover_data=['nombre_producto'],
        title='📊 Ticket Promedio vs Volumen de Órdenes',
        labels={
            'num_ordenes': 'Número de Órdenes',
            'ticket_promedio': 'Ticket Promedio ($)',
            'ingresos_totales': 'Ingresos'
        },
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=400)
    
    return fig


def plot_top_clientes(data):
    """Gráfico de top clientes por ingresos."""
    top_15 = data['metricas_cliente'].nlargest(15, 'ingresos_totales')
    
    fig = px.bar(
        top_15,
        x='ingresos_totales',
        y='nombre_empresa',
        orientation='h',
        title='🏆 Top 15 Clientes por Ingresos',
        labels={'ingresos_totales': 'Ingresos ($)', 'nombre_empresa': 'Cliente'},
        color='ingresos_totales',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=500, showlegend=False)
    
    return fig


def plot_ingresos_por_mes(data):
    """Gráfico de ingresos por mes."""
    df = data['metricas_cliente'].copy()
    df['mes'] = df['ultima_orden'].dt.to_period('M').astype(str)
    
    ingresos_mes = df.groupby('mes')['ingresos_totales'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=ingresos_mes['mes'],
        y=ingresos_mes['ingresos_totales'],
        name='Ingresos',
        marker=dict(color='#667eea')
    ))
    
    fig.update_layout(
        title='📈 Evolución de Ingresos Mensuales',
        xaxis_title='Mes',
        yaxis_title='Ingresos ($)',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def plot_concentracion_clientes(data):
    """Gráfico de concentración de ingresos."""
    # Ordenar por ingresos
    df = data['metricas_cliente'].sort_values('ingresos_totales', ascending=False)
    df['cliente_num'] = range(1, len(df) + 1)
    df['ingresos_acumulados'] = df['ingresos_totales'].cumsum()
    df['porcentaje_acumulado'] = (df['ingresos_acumulados'] / df['ingresos_totales'].sum() * 100)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['cliente_num'],
        y=df['porcentaje_acumulado'],
        mode='lines',
        name='Ingresos Acumulados',
        line=dict(color='#667eea', width=3),
        fill='tozeroy'
    ))
    
    # Línea de referencia 80/20
    fig.add_hline(y=80, line_dash="dash", line_color="red", 
                  annotation_text="80%", annotation_position="right")
    
    fig.update_layout(
        title='📊 Curva de Concentración de Ingresos (Pareto)',
        xaxis_title='Número de Clientes',
        yaxis_title='% Ingresos Acumulados',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def main():
    st.title("💰 Dashboard Financiero")
    st.markdown("---")
    
    # Cargar datos
    with st.spinner('Cargando datos financieros...'):
        kpis, data = load_data()
    
    # KPIs Financieros
    st.subheader("💵 KPIs Financieros")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi = kpis['financiero']['ingresos_totales']
        st.metric(
            "Ingresos Totales",
            f"${kpi['valor']:,.2f}"
        )
    
    with col2:
        kpi = kpis['financiero']['ingresos_mes']
        st.metric(
            "Ingresos del Mes",
            f"${kpi['valor']:,.2f}"
        )
    
    with col3:
        kpi = kpis['financiero']['ticket_promedio']
        st.metric(
            "Ticket Promedio",
            f"${kpi['valor']:,.2f}",
            f"Objetivo: ${kpi['objetivo']:,}"
        )
    
    with col4:
        kpi = kpis['financiero']['concentracion_top10']
        st.metric(
            "Concentración Top 10",
            f"{kpi['valor']:.1f}%",
            f"Objetivo: <{kpi['objetivo']}%"
        )
    
    st.markdown("---")
    
    # Visualizaciones
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_ingresos_por_producto(data), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_top_clientes(data), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_ingresos_por_mes(data), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_concentracion_clientes(data), use_container_width=True)
    
    st.markdown("---")
    
    # Análisis detallado
    st.subheader("📊 Análisis de Rentabilidad por Producto")
    
    st.plotly_chart(plot_ticket_vs_volumen(data), use_container_width=True)
    
    st.markdown("---")
    
    # Tabla de productos
    st.subheader("📋 Detalle de Ventas por Producto")
    
    st.dataframe(
        data['ventas_producto'].sort_values('ingresos_totales', ascending=False),
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()

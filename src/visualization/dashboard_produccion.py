"""
Dashboard de Producción - Trazamatic
Análisis de productividad, órdenes y empleados.
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
    page_title="Dashboard de Producción - Trazamatic",
    page_icon="🏭",
    layout="wide"
)


@st.cache_data(ttl=3600)
def load_data():
    """Carga datos de producción."""
    calculator = KPICalculator()
    kpis = calculator.calcular_todos_kpis()
    
    data = {
        'ordenes': pd.read_csv('data/analytics/ordenes_completas.csv'),
        'productividad': pd.read_csv('data/analytics/productividad_empleados.csv')
    }
    
    # Convertir fechas
    data['ordenes']['fecha_orden'] = pd.to_datetime(data['ordenes']['fecha_orden'])
    
    return kpis, data


def plot_productividad_empleados(data):
    """Gráfico de productividad por empleado."""
    top_15 = data['productividad'].nlargest(15, 'total_ordenes')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_15['nombre'],
        x=top_15['total_ordenes'],
        name='Total Órdenes',
        orientation='h',
        marker=dict(color='#667eea')
    ))
    
    fig.add_trace(go.Bar(
        y=top_15['nombre'],
        x=top_15['ordenes_completadas'],
        name='Completadas',
        orientation='h',
        marker=dict(color='#10b981')
    ))
    
    fig.update_layout(
        title='👥 Top 15 Empleados por Productividad',
        xaxis_title='Número de Órdenes',
        yaxis_title='Empleado',
        barmode='group',
        height=500,
        hovermode='y unified'
    )
    
    return fig


def plot_estados_timeline(data):
    """Gráfico de evolución de estados."""
    # Agrupar por mes y estado
    df = data['ordenes'].copy()
    df['mes'] = df['fecha_orden'].dt.to_period('M').astype(str)
    
    estados_mes = df.groupby(['mes', 'estado']).size().reset_index(name='cantidad')
    
    fig = px.bar(
        estados_mes,
        x='mes',
        y='cantidad',
        color='estado',
        title='📊 Evolución de Estados de Órdenes por Mes',
        labels={'mes': 'Mes', 'cantidad': 'Cantidad', 'estado': 'Estado'},
        color_discrete_map={
            'Completado': '#10b981',
            'En Proceso': '#f59e0b',
            'Pendiente': '#6b7280',
            'Cancelado': '#ef4444'
        }
    )
    
    fig.update_layout(height=400, barmode='stack')
    
    return fig


def plot_tasa_completitud_empleados(data):
    """Gráfico de tasa de completitud por empleado."""
    top_15 = data['productividad'].nlargest(15, 'total_ordenes')
    
    fig = px.scatter(
        top_15,
        x='total_ordenes',
        y='tasa_completitud',
        size='ordenes_completadas',
        color='tasa_completitud',
        hover_data=['nombre', 'cargo'],
        title='🎯 Tasa de Completitud vs Volumen de Órdenes',
        labels={
            'total_ordenes': 'Total de Órdenes',
            'tasa_completitud': 'Tasa de Completitud (%)',
            'ordenes_completadas': 'Completadas'
        },
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(height=400)
    
    return fig


def plot_ordenes_por_dia(data):
    """Gráfico de órdenes por día de la semana."""
    df = data['ordenes'].copy()
    df['dia_semana'] = df['fecha_orden'].dt.day_name()
    
    # Ordenar días de la semana
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    ordenes_dia = df['dia_semana'].value_counts().reindex(dias_orden, fill_value=0)
    ordenes_dia.index = dias_es
    
    fig = px.bar(
        x=ordenes_dia.index,
        y=ordenes_dia.values,
        title='📅 Distribución de Órdenes por Día de la Semana',
        labels={'x': 'Día', 'y': 'Número de Órdenes'},
        color=ordenes_dia.values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def main():
    st.title("🏭 Dashboard de Producción")
    st.markdown("---")
    
    # Cargar datos
    with st.spinner('Cargando datos de producción...'):
        kpis, data = load_data()
    
    # KPIs de Producción
    st.subheader("📊 KPIs de Producción")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        kpi = kpis['produccion']['tasa_completitud']
        st.metric(
            "Tasa de Completitud",
            f"{kpi['valor']:.1f}%",
            f"Objetivo: {kpi['objetivo']}%"
        )
    
    with col2:
        kpi = kpis['produccion']['tiempo_promedio']
        st.metric(
            "Tiempo Promedio",
            f"{kpi['valor']:.1f} días",
            f"Objetivo: <{kpi['objetivo']} días"
        )
    
    with col3:
        kpi = kpis['produccion']['productividad_empleado']
        st.metric(
            "Productividad/Empleado",
            f"{kpi['valor']:.1f}",
            f"Objetivo: >{kpi['objetivo']}"
        )
    
    with col4:
        kpi = kpis['produccion']['ordenes_en_proceso']
        st.metric(
            "Órdenes en Proceso",
            f"{kpi['valor']}"
        )
    
    st.markdown("---")
    
    # Visualizaciones
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_productividad_empleados(data), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_tasa_completitud_empleados(data), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_estados_timeline(data), use_container_width=True)
    
    with col2:
        st.plotly_chart(plot_ordenes_por_dia(data), use_container_width=True)
    
    st.markdown("---")
    
    # Tabla de empleados
    st.subheader("👥 Detalle de Productividad por Empleado")
    
    st.dataframe(
        data['productividad'].sort_values('total_ordenes', ascending=False),
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()

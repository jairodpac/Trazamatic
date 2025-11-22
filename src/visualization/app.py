"""
Aplicación Principal de Dashboards - Trazamatic
Punto de entrada para todos los dashboards analíticos.
"""

import streamlit as st

st.set_page_config(
    page_title="Trazamatic Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .dashboard-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<h1 class="main-title">📊 Trazamatic Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Sistema de Analíticos y KPIs para Gestión de Producción</p>', 
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Información del sistema
    st.subheader("🎯 Bienvenido al Sistema de Analíticos")
    
    st.markdown("""
    Este sistema proporciona análisis completos de tu operación de producción textil a través de múltiples dashboards especializados.
    
    ### Dashboards Disponibles:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="icon">📊</div>
            <h3>Dashboard Ejecutivo</h3>
            <p>Vista general con KPIs principales, tendencias de ingresos, top productos y distribución geográfica.</p>
            <ul>
                <li>KPIs principales</li>
                <li>Tendencias de ingresos</li>
                <li>Top 10 productos</li>
                <li>Distribución de estados</li>
                <li>Clientes por ciudad</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div class="icon">🏭</div>
            <h3>Dashboard de Producción</h3>
            <p>Análisis de productividad, órdenes y desempeño de empleados.</p>
            <ul>
                <li>Productividad por empleado</li>
                <li>Tasa de completitud</li>
                <li>Timeline de estados</li>
                <li>Órdenes por día</li>
                <li>Alertas de producción</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div class="icon">💰</div>
            <h3>Dashboard Financiero</h3>
            <p>Análisis de ingresos, costos y rentabilidad por producto y cliente.</p>
            <ul>
                <li>Ingresos por producto</li>
                <li>Top clientes</li>
                <li>Curva de Pareto</li>
                <li>Evolución mensual</li>
                <li>Análisis de rentabilidad</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Instrucciones
    st.subheader("🚀 Cómo Usar")
    
    st.markdown("""
    ### Para ejecutar los dashboards:
    
    1. **Dashboard Ejecutivo:**
       ```bash
       streamlit run src/visualization/dashboard_ejecutivo.py
       ```
    
    2. **Dashboard de Producción:**
       ```bash
       streamlit run src/visualization/dashboard_produccion.py
       ```
    
    3. **Dashboard Financiero:**
       ```bash
       streamlit run src/visualization/dashboard_financiero.py
       ```
    
    ### Actualización de Datos:
    
    Para actualizar los datos procesados y tablas analíticas, ejecuta:
    ```bash
    python src/etl.py
    ```
    
    Los dashboards se actualizarán automáticamente con los nuevos datos.
    """)
    
    st.markdown("---")
    
    # Información técnica
    with st.expander("ℹ️ Información Técnica"):
        st.markdown("""
        ### Arquitectura del Sistema
        
        - **ETL Pipeline:** Extracción, transformación y carga de datos
        - **Módulo de KPIs:** Cálculo de 15+ indicadores de negocio
        - **Dashboards Interactivos:** Visualizaciones con Streamlit y Plotly
        
        ### Datos Procesados
        
        - 7 datasets limpios en `data/processed/`
        - 5 tablas analíticas en `data/analytics/`
        - Actualización bajo demanda
        
        ### KPIs Disponibles
        
        **Producción:** Tasa de completitud, tiempo promedio, productividad, eficiencia
        
        **Financiero:** Ingresos totales, ticket promedio, concentración de clientes
        
        **Clientes:** Clientes activos, tasa de retención, frecuencia de compra
        
        **Inventario:** Rotación de materiales, stock crítico, materiales más usados
        """)
    
    # Footer
    st.markdown("---")
    st.caption("Trazamatic Analytics v1.0 | Desarrollado con Streamlit y Plotly")


if __name__ == "__main__":
    main()

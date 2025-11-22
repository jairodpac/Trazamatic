"""
Módulo de cálculo de KPIs
Implementa las funciones para calcular todos los KPIs definidos en el plan.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KPICalculator:
    """Clase para calcular KPIs de negocio."""
    
    def __init__(self, data_dir: str = "data/analytics"):
        """
        Inicializa el calculador de KPIs.
        
        Args:
            data_dir: Directorio donde se encuentran las tablas analíticas
        """
        self.data_dir = data_dir
        self.load_data()
    
    def load_data(self):
        """Carga las tablas analíticas necesarias."""
        try:
            # Cargar órdenes completas con fechas opcionales
            self.ordenes_completas = pd.read_csv(
                f"{self.data_dir}/ordenes_completas.csv"
            )
            # Convertir fechas si existen
            date_columns = ['fecha_orden', 'fecha_completado']
            for col in date_columns:
                if col in self.ordenes_completas.columns:
                    self.ordenes_completas[col] = pd.to_datetime(
                        self.ordenes_completas[col], errors='coerce'
                    )
            
            self.ventas_por_producto = pd.read_csv(
                f"{self.data_dir}/ventas_por_producto.csv"
            )
            self.metricas_por_cliente = pd.read_csv(
                f"{self.data_dir}/metricas_por_cliente.csv",
                parse_dates=['primera_orden', 'ultima_orden']
            )
            self.productividad_empleados = pd.read_csv(
                f"{self.data_dir}/productividad_empleados.csv"
            )
            self.uso_materiales_agregado = pd.read_csv(
                f"{self.data_dir}/uso_materiales_agregado.csv"
            )
            logger.info("✓ Datos analíticos cargados exitosamente")
        except Exception as e:
            logger.error(f"Error al cargar datos: {str(e)}")
            raise
    
    # ========== KPIs DE PRODUCCIÓN ==========
    
    def kpi_tasa_completitud_ordenes(self) -> Dict:
        """
        Calcula la tasa de completitud de órdenes.
        Objetivo: > 85%
        """
        total_ordenes = len(self.ordenes_completas)
        ordenes_completadas = (self.ordenes_completas['estado'] == 'Completado').sum()
        tasa = (ordenes_completadas / total_ordenes * 100) if total_ordenes > 0 else 0
        
        return {
            'nombre': 'Tasa de Completitud de Órdenes',
            'valor': round(tasa, 2),
            'unidad': '%',
            'objetivo': 85,
            'cumple_objetivo': tasa >= 85,
            'ordenes_completadas': ordenes_completadas,
            'total_ordenes': total_ordenes
        }
    
    def kpi_tiempo_promedio_produccion(self) -> Dict:
        """
        Calcula el tiempo promedio de producción en días.
        Objetivo: < 15 días
        """
        ordenes_completadas = self.ordenes_completas[
            self.ordenes_completas['estado'] == 'Completado'
        ].copy()
        
        if 'duracion_dias' in ordenes_completadas.columns:
            tiempo_promedio = ordenes_completadas['duracion_dias'].mean()
        else:
            tiempo_promedio = 0
        
        return {
            'nombre': 'Tiempo Promedio de Producción',
            'valor': round(tiempo_promedio, 1),
            'unidad': 'días',
            'objetivo': 15,
            'cumple_objetivo': tiempo_promedio < 15,
            'ordenes_analizadas': len(ordenes_completadas)
        }
    
    def kpi_productividad_por_empleado(self) -> Dict:
        """
        Calcula órdenes promedio por empleado.
        Objetivo: > 5 órdenes/mes
        """
        ordenes_por_empleado = self.productividad_empleados['total_ordenes'].mean()
        
        return {
            'nombre': 'Productividad por Empleado',
            'valor': round(ordenes_por_empleado, 1),
            'unidad': 'órdenes/empleado',
            'objetivo': 5,
            'cumple_objetivo': ordenes_por_empleado > 5,
            'total_empleados': len(self.productividad_empleados)
        }
    
    def kpi_eficiencia_uso_materiales(self) -> Dict:
        """
        Calcula la eficiencia de uso de materiales.
        Objetivo: 70-85%
        """
        tasa_promedio = self.uso_materiales_agregado['tasa_rotacion'].mean() * 100
        
        return {
            'nombre': 'Eficiencia de Uso de Materiales',
            'valor': round(tasa_promedio, 2),
            'unidad': '%',
            'objetivo_min': 70,
            'objetivo_max': 85,
            'cumple_objetivo': 70 <= tasa_promedio <= 85
        }
    
    def kpi_ordenes_en_proceso(self) -> Dict:
        """Calcula cantidad de órdenes en proceso."""
        en_proceso = (self.ordenes_completas['estado'] == 'En Proceso').sum()
        
        return {
            'nombre': 'Órdenes en Proceso',
            'valor': en_proceso,
            'unidad': 'órdenes',
            'tipo': 'monitoreo'
        }
    
    # ========== KPIs FINANCIEROS ==========
    
    def kpi_ingresos_totales(self, periodo_dias: Optional[int] = 30) -> Dict:
        """
        Calcula ingresos totales del período.
        
        Args:
            periodo_dias: Días a considerar (None = todos)
        """
        if periodo_dias:
            fecha_limite = datetime.now() - timedelta(days=periodo_dias)
            clientes_periodo = self.metricas_por_cliente[
                self.metricas_por_cliente['ultima_orden'] >= fecha_limite
            ]
            ingresos = clientes_periodo['ingresos_totales'].sum()
        else:
            ingresos = self.metricas_por_cliente['ingresos_totales'].sum()
        
        return {
            'nombre': f'Ingresos Totales ({periodo_dias} días)' if periodo_dias else 'Ingresos Totales',
            'valor': round(ingresos, 2),
            'unidad': '$',
            'periodo_dias': periodo_dias
        }
    
    def kpi_ticket_promedio(self) -> Dict:
        """
        Calcula el ticket promedio por orden.
        Objetivo: > $5,000
        """
        ticket_promedio = self.metricas_por_cliente['ticket_promedio'].mean()
        
        return {
            'nombre': 'Ticket Promedio',
            'valor': round(ticket_promedio, 2),
            'unidad': '$',
            'objetivo': 5000,
            'cumple_objetivo': ticket_promedio > 5000
        }
    
    def kpi_ingresos_por_cliente_top(self, top_n: int = 10) -> Dict:
        """
        Analiza concentración de ingresos en top clientes.
        Objetivo: Top 10 < 50% de ingresos totales
        """
        total_ingresos = self.metricas_por_cliente['ingresos_totales'].sum()
        top_clientes = self.metricas_por_cliente.nlargest(top_n, 'ingresos_totales')
        ingresos_top = top_clientes['ingresos_totales'].sum()
        porcentaje = (ingresos_top / total_ingresos * 100) if total_ingresos > 0 else 0
        
        return {
            'nombre': f'Concentración Top {top_n} Clientes',
            'valor': round(porcentaje, 2),
            'unidad': '%',
            'objetivo': 50,
            'cumple_objetivo': porcentaje < 50,
            'ingresos_top': round(ingresos_top, 2),
            'total_ingresos': round(total_ingresos, 2)
        }
    
    # ========== KPIs DE CLIENTES ==========
    
    def kpi_clientes_activos(self, dias: int = 90) -> Dict:
        """
        Calcula clientes activos en los últimos N días.
        
        Args:
            dias: Días a considerar para cliente activo
        """
        fecha_limite = datetime.now() - timedelta(days=dias)
        clientes_activos = (
            self.metricas_por_cliente['ultima_orden'] >= fecha_limite
        ).sum()
        
        return {
            'nombre': f'Clientes Activos ({dias} días)',
            'valor': clientes_activos,
            'unidad': 'clientes',
            'periodo_dias': dias,
            'total_clientes': len(self.metricas_por_cliente)
        }
    
    def kpi_tasa_retencion(self) -> Dict:
        """
        Calcula tasa de retención (clientes con más de 1 orden).
        Objetivo: > 60%
        """
        clientes_recurrentes = (self.metricas_por_cliente['num_ordenes'] > 1).sum()
        total_clientes = len(self.metricas_por_cliente)
        tasa = (clientes_recurrentes / total_clientes * 100) if total_clientes > 0 else 0
        
        return {
            'nombre': 'Tasa de Retención',
            'valor': round(tasa, 2),
            'unidad': '%',
            'objetivo': 60,
            'cumple_objetivo': tasa > 60,
            'clientes_recurrentes': clientes_recurrentes,
            'total_clientes': total_clientes
        }
    
    def kpi_frecuencia_compra(self) -> Dict:
        """
        Calcula frecuencia promedio de compra.
        Objetivo: > 3 órdenes/año
        """
        frecuencia = self.metricas_por_cliente['num_ordenes'].mean()
        
        return {
            'nombre': 'Frecuencia de Compra',
            'valor': round(frecuencia, 2),
            'unidad': 'órdenes/cliente',
            'objetivo': 3,
            'cumple_objetivo': frecuencia > 3
        }
    
    def kpi_distribucion_geografica(self) -> Dict:
        """Calcula distribución de clientes por ciudad."""
        distribucion = self.metricas_por_cliente['ciudad'].value_counts().to_dict()
        
        return {
            'nombre': 'Distribución Geográfica',
            'valor': distribucion,
            'tipo': 'distribucion',
            'total_ciudades': len(distribucion)
        }
    
    # ========== KPIs DE INVENTARIO ==========
    
    def kpi_rotacion_materiales(self) -> Dict:
        """
        Calcula rotación promedio de materiales.
        Objetivo: > 4 veces/año
        """
        rotacion_promedio = self.uso_materiales_agregado['tasa_rotacion'].mean()
        
        return {
            'nombre': 'Rotación de Materiales',
            'valor': round(rotacion_promedio, 2),
            'unidad': 'veces',
            'objetivo': 4,
            'cumple_objetivo': rotacion_promedio > 4
        }
    
    def kpi_stock_critico(self, umbral_porcentaje: float = 20) -> Dict:
        """
        Identifica materiales con stock crítico.
        Objetivo: 0 materiales
        """
        # Calcular porcentaje de stock restante
        self.uso_materiales_agregado['stock_restante_pct'] = (
            (self.uso_materiales_agregado['cantidad_disponible'] - 
             self.uso_materiales_agregado['cantidad_total_usada']) /
            self.uso_materiales_agregado['cantidad_disponible'] * 100
        ).fillna(100)
        
        materiales_criticos = (
            self.uso_materiales_agregado['stock_restante_pct'] < umbral_porcentaje
        ).sum()
        
        return {
            'nombre': 'Materiales con Stock Crítico',
            'valor': materiales_criticos,
            'unidad': 'materiales',
            'objetivo': 0,
            'cumple_objetivo': materiales_criticos == 0,
            'umbral_porcentaje': umbral_porcentaje
        }
    
    def kpi_materiales_mas_usados(self, top_n: int = 10) -> Dict:
        """Identifica los materiales más usados."""
        top_materiales = self.uso_materiales_agregado.nlargest(
            top_n, 'cantidad_total_usada'
        )[['nombre_material', 'tipo', 'cantidad_total_usada']].to_dict('records')
        
        return {
            'nombre': f'Top {top_n} Materiales Más Usados',
            'valor': top_materiales,
            'tipo': 'ranking'
        }
    
    # ========== MÉTODO PARA CALCULAR TODOS LOS KPIs ==========
    
    def calcular_todos_kpis(self) -> Dict:
        """Calcula todos los KPIs y retorna un diccionario."""
        logger.info("=" * 60)
        logger.info("CALCULANDO TODOS LOS KPIs")
        logger.info("=" * 60)
        
        kpis = {
            # Producción
            'produccion': {
                'tasa_completitud': self.kpi_tasa_completitud_ordenes(),
                'tiempo_promedio': self.kpi_tiempo_promedio_produccion(),
                'productividad_empleado': self.kpi_productividad_por_empleado(),
                'eficiencia_materiales': self.kpi_eficiencia_uso_materiales(),
                'ordenes_en_proceso': self.kpi_ordenes_en_proceso()
            },
            # Financiero
            'financiero': {
                'ingresos_totales': self.kpi_ingresos_totales(),
                'ingresos_mes': self.kpi_ingresos_totales(periodo_dias=30),
                'ticket_promedio': self.kpi_ticket_promedio(),
                'concentracion_top10': self.kpi_ingresos_por_cliente_top(10)
            },
            # Clientes
            'clientes': {
                'activos_90dias': self.kpi_clientes_activos(90),
                'tasa_retencion': self.kpi_tasa_retencion(),
                'frecuencia_compra': self.kpi_frecuencia_compra(),
                'distribucion_geografica': self.kpi_distribucion_geografica()
            },
            # Inventario
            'inventario': {
                'rotacion_materiales': self.kpi_rotacion_materiales(),
                'stock_critico': self.kpi_stock_critico(),
                'materiales_mas_usados': self.kpi_materiales_mas_usados(10)
            }
        }
        
        logger.info("✓ Todos los KPIs calculados exitosamente")
        return kpis


if __name__ == "__main__":
    # Test del módulo
    calculator = KPICalculator()
    kpis = calculator.calcular_todos_kpis()
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE KPIs")
    print("=" * 60)
    
    for categoria, kpis_cat in kpis.items():
        print(f"\n{categoria.upper()}:")
        for nombre, kpi in kpis_cat.items():
            if 'valor' in kpi and 'unidad' in kpi:
                print(f"  • {kpi['nombre']}: {kpi['valor']} {kpi['unidad']}")

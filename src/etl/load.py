"""
Módulo de carga de datos (Load)
Guarda los datos procesados y crea tablas analíticas agregadas.
"""

import pandas as pd
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Clase para cargar datos procesados y crear tablas analíticas."""
    
    def __init__(self, processed_dir: str = "data/processed", 
                 analytics_dir: str = "data/analytics"):
        """
        Inicializa el cargador de datos.
        
        Args:
            processed_dir: Directorio para datos procesados
            analytics_dir: Directorio para tablas analíticas
        """
        self.processed_dir = Path(processed_dir)
        self.analytics_dir = Path(analytics_dir)
        
        # Crear directorios si no existen
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.analytics_dir.mkdir(parents=True, exist_ok=True)
    
    def save_processed(self, datasets: dict) -> None:
        """
        Guarda los datasets procesados como CSV.
        
        Args:
            datasets: Diccionario con DataFrames procesados
        """
        logger.info("=" * 60)
        logger.info("GUARDANDO DATOS PROCESADOS")
        logger.info("=" * 60)
        
        for name, df in datasets.items():
            filepath = self.processed_dir / f"{name}_limpio.csv"
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"✓ Guardado: {filepath.name} ({len(df)} registros)")
        
        logger.info(f"✓ {len(datasets)} archivos guardados en {self.processed_dir}")
    
    def create_analytics_tables(self, datasets: dict) -> dict:
        """
        Crea tablas analíticas agregadas para dashboards.
        
        Args:
            datasets: Diccionario con DataFrames procesados
            
        Returns:
            Diccionario con tablas analíticas
        """
        logger.info("=" * 60)
        logger.info("CREANDO TABLAS ANALÍTICAS")
        logger.info("=" * 60)
        
        analytics = {}
        
        # Tabla: Órdenes completas (join de múltiples tablas)
        if all(k in datasets for k in ['ordenes_produccion', 'clientes', 'empleados']):
            analytics['ordenes_completas'] = self._create_ordenes_completas(
                datasets['ordenes_produccion'],
                datasets['clientes'],
                datasets['empleados']
            )
        
        # Tabla: Ventas por producto
        if all(k in datasets for k in ['detalles_orden', 'productos', 'ordenes_produccion']):
            analytics['ventas_por_producto'] = self._create_ventas_por_producto(
                datasets['detalles_orden'],
                datasets['productos'],
                datasets['ordenes_produccion']
            )
        
        # Tabla: Uso de materiales agregado
        if all(k in datasets for k in ['uso_materiales', 'materiales', 'ordenes_produccion']):
            analytics['uso_materiales_agregado'] = self._create_uso_materiales_agregado(
                datasets['uso_materiales'],
                datasets['materiales'],
                datasets['ordenes_produccion']
            )
        
        # Tabla: Métricas por cliente
        if all(k in datasets for k in ['ordenes_produccion', 'detalles_orden', 'clientes']):
            analytics['metricas_por_cliente'] = self._create_metricas_por_cliente(
                datasets['ordenes_produccion'],
                datasets['detalles_orden'],
                datasets['clientes']
            )
        
        # Tabla: Productividad por empleado
        if all(k in datasets for k in ['ordenes_produccion', 'empleados']):
            analytics['productividad_empleados'] = self._create_productividad_empleados(
                datasets['ordenes_produccion'],
                datasets['empleados']
            )
        
        logger.info(f"✓ {len(analytics)} tablas analíticas creadas")
        return analytics
    
    def _create_ordenes_completas(self, ordenes: pd.DataFrame, 
                                   clientes: pd.DataFrame,
                                   empleados: pd.DataFrame) -> pd.DataFrame:
        """Crea tabla de órdenes con información completa."""
        logger.info("Creando tabla: ordenes_completas")
        
        # Join con clientes
        df = ordenes.merge(
            clientes[['id_cliente', 'nombre_empresa', 'ciudad']],
            on='id_cliente',
            how='left'
        )
        
        # Join con empleados
        df = df.merge(
            empleados[['id_empleado', 'nombre', 'cargo']],
            left_on='id_empleado_responsable',
            right_on='id_empleado',
            how='left',
            suffixes=('', '_empleado')
        )
        
        # Renombrar columnas
        df = df.rename(columns={
            'nombre': 'nombre_empleado',
            'cargo': 'cargo_empleado'
        })
        
        return df
    
    def _create_ventas_por_producto(self, detalles: pd.DataFrame,
                                     productos: pd.DataFrame,
                                     ordenes: pd.DataFrame) -> pd.DataFrame:
        """Crea tabla de ventas agregadas por producto."""
        logger.info("Creando tabla: ventas_por_producto")
        
        # Join detalles con productos (solo usar columnas que existen)
        df = detalles.merge(
            productos[['id_producto', 'nombre_producto']],
            on='id_producto',
            how='left'
        )
        
        # Join con órdenes para obtener fechas
        df = df.merge(
            ordenes[['id_orden', 'fecha_orden', 'estado']],
            on='id_orden',
            how='left'
        )
        
        # Agregar por producto
        ventas = df.groupby('id_producto').agg({
            'nombre_producto': 'first',
            'cantidad': 'sum',
            'subtotal': 'sum',
            'id_orden': 'count'
        }).reset_index()
        
        ventas = ventas.rename(columns={
            'cantidad': 'cantidad_total',
            'subtotal': 'ingresos_totales',
            'id_orden': 'num_ordenes'
        })
        
        ventas['ticket_promedio'] = ventas['ingresos_totales'] / ventas['num_ordenes']
        
        return ventas
    
    def _create_uso_materiales_agregado(self, uso: pd.DataFrame,
                                         materiales: pd.DataFrame,
                                         ordenes: pd.DataFrame) -> pd.DataFrame:
        """Crea tabla de uso de materiales agregado."""
        logger.info("Creando tabla: uso_materiales_agregado")
        
        # Join con materiales
        df = uso.merge(
            materiales[['id_material', 'nombre_material', 'tipo', 'cantidad_disponible']],
            on='id_material',
            how='left'
        )
        
        # Join con órdenes para fechas
        df = df.merge(
            ordenes[['id_orden', 'fecha_orden']],
            on='id_orden',
            how='left'
        )
        
        # Agregar por material
        uso_agg = df.groupby('id_material').agg({
            'nombre_material': 'first',
            'tipo': 'first',
            'cantidad_disponible': 'first',
            'cantidad_usada': 'sum',
            'id_orden': 'count'
        }).reset_index()
        
        uso_agg = uso_agg.rename(columns={
            'cantidad_usada': 'cantidad_total_usada',
            'id_orden': 'num_ordenes'
        })
        
        # Calcular tasa de rotación
        uso_agg['tasa_rotacion'] = (
            uso_agg['cantidad_total_usada'] / uso_agg['cantidad_disponible']
        ).fillna(0)
        
        return uso_agg
    
    def _create_metricas_por_cliente(self, ordenes: pd.DataFrame,
                                      detalles: pd.DataFrame,
                                      clientes: pd.DataFrame) -> pd.DataFrame:
        """Crea tabla de métricas por cliente."""
        logger.info("Creando tabla: metricas_por_cliente")
        
        # Calcular total por orden
        totales_orden = detalles.groupby('id_orden').agg({
            'subtotal': 'sum'
        }).reset_index()
        totales_orden = totales_orden.rename(columns={'subtotal': 'total_orden'})
        
        # Join órdenes con totales
        df = ordenes.merge(totales_orden, on='id_orden', how='left')
        
        # Agregar por cliente
        metricas = df.groupby('id_cliente').agg({
            'id_orden': 'count',
            'total_orden': 'sum',
            'fecha_orden': ['min', 'max']
        }).reset_index()
        
        metricas.columns = ['id_cliente', 'num_ordenes', 'ingresos_totales', 
                           'primera_orden', 'ultima_orden']
        
        # Join con información del cliente
        metricas = metricas.merge(
            clientes[['id_cliente', 'nombre_empresa', 'ciudad']],
            on='id_cliente',
            how='left'
        )
        
        # Calcular métricas adicionales
        metricas['ticket_promedio'] = metricas['ingresos_totales'] / metricas['num_ordenes']
        
        return metricas
    
    def _create_productividad_empleados(self, ordenes: pd.DataFrame,
                                        empleados: pd.DataFrame) -> pd.DataFrame:
        """Crea tabla de productividad por empleado."""
        logger.info("Creando tabla: productividad_empleados")
        
        # Agregar órdenes por empleado
        prod = ordenes.groupby('id_empleado_responsable').agg({
            'id_orden': 'count',
            'estado': lambda x: (x == 'Completado').sum()
        }).reset_index()
        
        prod.columns = ['id_empleado', 'total_ordenes', 'ordenes_completadas']
        
        # Join con empleados
        prod = prod.merge(
            empleados[['id_empleado', 'nombre', 'cargo']],
            on='id_empleado',
            how='left'
        )
        
        # Calcular tasa de completitud
        prod['tasa_completitud'] = (
            prod['ordenes_completadas'] / prod['total_ordenes'] * 100
        ).round(2)
        
        return prod
    
    def save_analytics(self, analytics: dict) -> None:
        """
        Guarda las tablas analíticas como CSV.
        
        Args:
            analytics: Diccionario con tablas analíticas
        """
        logger.info("=" * 60)
        logger.info("GUARDANDO TABLAS ANALÍTICAS")
        logger.info("=" * 60)
        
        for name, df in analytics.items():
            filepath = self.analytics_dir / f"{name}.csv"
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"✓ Guardado: {filepath.name} ({len(df)} registros)")
        
        logger.info(f"✓ {len(analytics)} tablas guardadas en {self.analytics_dir}")


if __name__ == "__main__":
    # Test del módulo
    from extract import DataExtractor
    from transform import DataTransformer
    
    extractor = DataExtractor()
    raw_data = extractor.extract_all()
    
    transformer = DataTransformer()
    clean_data = transformer.transform_all(raw_data)
    
    loader = DataLoader()
    loader.save_processed(clean_data)
    
    analytics = loader.create_analytics_tables(clean_data)
    loader.save_analytics(analytics)
    
    print("\nTablas analíticas creadas:")
    for name, df in analytics.items():
        print(f"  {name}: {len(df)} filas, {len(df.columns)} columnas")

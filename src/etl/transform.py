"""
Módulo de transformación de datos (Transform)
Limpia y transforma los datos extraídos para análisis.
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformer:
    """Clase para transformar y limpiar datos."""
    
    def __init__(self):
        """Inicializa el transformador de datos."""
        pass
    
    def transform_clientes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma y limpia datos de clientes.
        Basado en el notebook clientes.ipynb existente.
        
        Args:
            df: DataFrame de clientes raw
            
        Returns:
            DataFrame de clientes limpio
        """
        logger.info("Transformando clientes...")
        df_clean = df.copy()
        
        # Renombrar columnas para mayor claridad
        df_clean = df_clean.rename(columns={
            'contacto_telefono': 'telefono',
            'contacto_email': 'email',
            'contacto_nombre': 'nombre_contacto'
        })
        
        # Limpiar teléfonos: eliminar espacios y caracteres no numéricos
        if 'telefono' in df_clean.columns:
            df_clean['telefono'] = df_clean['telefono'].str.strip()
            df_clean['telefono'] = df_clean['telefono'].str.replace(r'\D', '', regex=True)
        
        # Limpiar emails duplicados
        duplicated_emails = df_clean['email'].duplicated(keep=False)
        if duplicated_emails.sum() > 0:
            logger.warning(f"Se encontraron {duplicated_emails.sum()} emails duplicados")
            # Agregar sufijo a duplicados
            for idx in df_clean[duplicated_emails].index[1:]:
                original_email = df_clean.at[idx, 'email']
                if '@' in original_email:
                    name, domain = original_email.split('@')
                    df_clean.at[idx, 'email'] = f"{name}{idx}@{domain}"
        
        # Limpiar espacios en strings
        string_columns = df_clean.select_dtypes(include=['object']).columns
        for col in string_columns:
            df_clean[col] = df_clean[col].str.strip()
        
        logger.info(f"✓ Clientes transformados: {len(df_clean)} registros")
        return df_clean
    
    def transform_ordenes_produccion(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma y limpia datos de órdenes de producción.
        
        Args:
            df: DataFrame de órdenes raw
            
        Returns:
            DataFrame de órdenes limpio
        """
        logger.info("Transformando órdenes de producción...")
        df_clean = df.copy()
        
        # Convertir fechas a datetime
        date_columns = [col for col in df_clean.columns if 'fecha' in col.lower()]
        for col in date_columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        
        # Estandarizar estados
        if 'estado' in df_clean.columns:
            df_clean['estado'] = df_clean['estado'].str.strip().str.title()
        
        # Calcular duración de orden (si hay fecha de inicio y fin)
        if 'fecha_orden' in df_clean.columns and 'fecha_completado' in df_clean.columns:
            df_clean['duracion_dias'] = (
                df_clean['fecha_completado'] - df_clean['fecha_orden']
            ).dt.days
        
        logger.info(f"✓ Órdenes transformadas: {len(df_clean)} registros")
        return df_clean
    
    def transform_productos(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma y limpia datos de productos.
        
        Args:
            df: DataFrame de productos raw
            
        Returns:
            DataFrame de productos limpio
        """
        logger.info("Transformando productos...")
        df_clean = df.copy()
        
        # Limpiar nombres de productos
        if 'nombre_producto' in df_clean.columns:
            df_clean['nombre_producto'] = df_clean['nombre_producto'].str.strip()
        
        # Asegurar que precio sea numérico
        if 'precio' in df_clean.columns:
            df_clean['precio'] = pd.to_numeric(df_clean['precio'], errors='coerce')
        
        # Eliminar productos con precio negativo o cero
        if 'precio' in df_clean.columns:
            invalid_prices = (df_clean['precio'] <= 0) | (df_clean['precio'].isna())
            if invalid_prices.sum() > 0:
                logger.warning(f"Eliminando {invalid_prices.sum()} productos con precio inválido")
                df_clean = df_clean[~invalid_prices]
        
        logger.info(f"✓ Productos transformados: {len(df_clean)} registros")
        return df_clean
    
    def transform_materiales(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma y limpia datos de materiales.
        
        Args:
            df: DataFrame de materiales raw
            
        Returns:
            DataFrame de materiales limpio
        """
        logger.info("Transformando materiales...")
        df_clean = df.copy()
        
        # Estandarizar tipos de material
        if 'tipo' in df_clean.columns:
            df_clean['tipo'] = df_clean['tipo'].str.strip().str.title()
        
        # Estandarizar unidades de medida
        if 'unidad_medida' in df_clean.columns:
            df_clean['unidad_medida'] = df_clean['unidad_medida'].str.strip().str.lower()
        
        # Asegurar que cantidad disponible sea numérica y positiva
        if 'cantidad_disponible' in df_clean.columns:
            df_clean['cantidad_disponible'] = pd.to_numeric(
                df_clean['cantidad_disponible'], errors='coerce'
            )
            df_clean['cantidad_disponible'] = df_clean['cantidad_disponible'].fillna(0)
        
        logger.info(f"✓ Materiales transformados: {len(df_clean)} registros")
        return df_clean
    
    def transform_empleados(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma y limpia datos de empleados.
        
        Args:
            df: DataFrame de empleados raw
            
        Returns:
            DataFrame de empleados limpio
        """
        logger.info("Transformando empleados...")
        df_clean = df.copy()
        
        # Limpiar nombres
        if 'nombre' in df_clean.columns:
            df_clean['nombre'] = df_clean['nombre'].str.strip()
        
        # Estandarizar cargos
        if 'cargo' in df_clean.columns:
            df_clean['cargo'] = df_clean['cargo'].str.strip().str.title()
        
        # Limpiar emails
        if 'email' in df_clean.columns:
            df_clean['email'] = df_clean['email'].str.strip().str.lower()
        
        logger.info(f"✓ Empleados transformados: {len(df_clean)} registros")
        return df_clean
    
    def transform_detalles_orden(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma y limpia datos de detalles de orden.
        
        Args:
            df: DataFrame de detalles raw
            
        Returns:
            DataFrame de detalles limpio
        """
        logger.info("Transformando detalles de orden...")
        df_clean = df.copy()
        
        # Asegurar que cantidad y subtotal sean numéricos
        numeric_columns = ['cantidad', 'subtotal']
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Calcular precio unitario si no existe
        if 'cantidad' in df_clean.columns and 'subtotal' in df_clean.columns:
            df_clean['precio_unitario'] = df_clean['subtotal'] / df_clean['cantidad']
        
        logger.info(f"✓ Detalles de orden transformados: {len(df_clean)} registros")
        return df_clean
    
    def transform_uso_materiales(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma y limpia datos de uso de materiales.
        
        Args:
            df: DataFrame de uso de materiales raw
            
        Returns:
            DataFrame de uso de materiales limpio
        """
        logger.info("Transformando uso de materiales...")
        df_clean = df.copy()
        
        # Asegurar que cantidad usada sea numérica
        if 'cantidad_usada' in df_clean.columns:
            df_clean['cantidad_usada'] = pd.to_numeric(
                df_clean['cantidad_usada'], errors='coerce'
            )
            df_clean['cantidad_usada'] = df_clean['cantidad_usada'].fillna(0)
        
        logger.info(f"✓ Uso de materiales transformado: {len(df_clean)} registros")
        return df_clean
    
    def transform_all(self, datasets: dict) -> dict:
        """
        Transforma todos los datasets.
        
        Args:
            datasets: Diccionario con DataFrames raw
            
        Returns:
            Diccionario con DataFrames transformados
        """
        logger.info("=" * 60)
        logger.info("INICIANDO TRANSFORMACIÓN DE DATOS")
        logger.info("=" * 60)
        
        transformed = {}
        
        if 'clientes' in datasets:
            transformed['clientes'] = self.transform_clientes(datasets['clientes'])
        
        if 'ordenes_produccion' in datasets:
            transformed['ordenes_produccion'] = self.transform_ordenes_produccion(
                datasets['ordenes_produccion']
            )
        
        if 'productos' in datasets:
            transformed['productos'] = self.transform_productos(datasets['productos'])
        
        if 'materiales' in datasets:
            transformed['materiales'] = self.transform_materiales(datasets['materiales'])
        
        if 'empleados' in datasets:
            transformed['empleados'] = self.transform_empleados(datasets['empleados'])
        
        if 'detalles_orden' in datasets:
            transformed['detalles_orden'] = self.transform_detalles_orden(
                datasets['detalles_orden']
            )
        
        if 'uso_materiales' in datasets:
            transformed['uso_materiales'] = self.transform_uso_materiales(
                datasets['uso_materiales']
            )
        
        logger.info("=" * 60)
        logger.info(f"TRANSFORMACIÓN COMPLETADA: {len(transformed)} datasets")
        logger.info("=" * 60)
        
        return transformed


if __name__ == "__main__":
    # Test del módulo
    from extract import DataExtractor
    
    extractor = DataExtractor()
    raw_data = extractor.extract_all()
    
    transformer = DataTransformer()
    clean_data = transformer.transform_all(raw_data)
    
    print("\nResumen de datos transformados:")
    for name, df in clean_data.items():
        print(f"  {name}: {len(df)} filas, {len(df.columns)} columnas")

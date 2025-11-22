"""
Módulo de extracción de datos (Extract)
Carga los datos raw desde archivos CSV con manejo de errores y validación.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    """Clase para extraer datos de archivos CSV raw."""
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Inicializa el extractor de datos.
        
        Args:
            data_dir: Directorio donde se encuentran los archivos CSV raw
        """
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"El directorio {data_dir} no existe")
    
    def _load_csv(self, filename: str, encoding: str = 'utf-8') -> Optional[pd.DataFrame]:
        """
        Carga un archivo CSV con manejo de errores.
        
        Args:
            filename: Nombre del archivo CSV
            encoding: Codificación del archivo
            
        Returns:
            DataFrame con los datos o None si hay error
        """
        filepath = self.data_dir / filename
        
        try:
            logger.info(f"Cargando {filename}...")
            df = pd.read_csv(filepath, encoding=encoding)
            logger.info(f"✓ {filename} cargado: {len(df)} registros, {len(df.columns)} columnas")
            return df
        except FileNotFoundError:
            logger.error(f"✗ Archivo no encontrado: {filepath}")
            return None
        except Exception as e:
            logger.error(f"✗ Error al cargar {filename}: {str(e)}")
            return None
    
    def extract_clientes(self) -> Optional[pd.DataFrame]:
        """Extrae datos de clientes."""
        return self._load_csv('clientes.csv')
    
    def extract_ordenes_produccion(self) -> Optional[pd.DataFrame]:
        """Extrae datos de órdenes de producción."""
        return self._load_csv('ordenes_produccion.csv')
    
    def extract_productos(self) -> Optional[pd.DataFrame]:
        """Extrae datos de productos."""
        return self._load_csv('productos.csv')
    
    def extract_materiales(self) -> Optional[pd.DataFrame]:
        """Extrae datos de materiales."""
        return self._load_csv('materiales.csv')
    
    def extract_empleados(self) -> Optional[pd.DataFrame]:
        """Extrae datos de empleados."""
        return self._load_csv('empleados.csv')
    
    def extract_detalles_orden(self) -> Optional[pd.DataFrame]:
        """Extrae datos de detalles de orden."""
        return self._load_csv('detalles_orden.csv')
    
    def extract_uso_materiales(self) -> Optional[pd.DataFrame]:
        """Extrae datos de uso de materiales."""
        return self._load_csv('uso_materiales.csv')
    
    def extract_all(self) -> dict:
        """
        Extrae todos los datasets disponibles.
        
        Returns:
            Diccionario con todos los DataFrames cargados
        """
        logger.info("=" * 60)
        logger.info("INICIANDO EXTRACCIÓN DE DATOS")
        logger.info("=" * 60)
        
        datasets = {
            'clientes': self.extract_clientes(),
            'ordenes_produccion': self.extract_ordenes_produccion(),
            'productos': self.extract_productos(),
            'materiales': self.extract_materiales(),
            'empleados': self.extract_empleados(),
            'detalles_orden': self.extract_detalles_orden(),
            'uso_materiales': self.extract_uso_materiales()
        }
        
        # Filtrar datasets que no se pudieron cargar
        datasets = {k: v for k, v in datasets.items() if v is not None}
        
        logger.info("=" * 60)
        logger.info(f"EXTRACCIÓN COMPLETADA: {len(datasets)}/7 datasets cargados")
        logger.info("=" * 60)
        
        return datasets


if __name__ == "__main__":
    # Test del módulo
    extractor = DataExtractor()
    data = extractor.extract_all()
    
    # Mostrar resumen
    print("\nResumen de datos extraídos:")
    for name, df in data.items():
        print(f"  {name}: {len(df)} filas, {len(df.columns)} columnas")

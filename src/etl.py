"""
Script principal del proceso ETL
Orquesta la extracción, transformación y carga de datos.
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.load import DataLoader
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_etl():
    """Ejecuta el proceso ETL completo."""
    try:
        logger.info("=" * 80)
        logger.info("INICIANDO PROCESO ETL COMPLETO - TRAZAMATIC")
        logger.info("=" * 80)
        
        # FASE 1: EXTRACCIÓN
        logger.info("\n[FASE 1/3] EXTRACCIÓN DE DATOS")
        extractor = DataExtractor(data_dir="data/raw")
        raw_data = extractor.extract_all()
        
        if not raw_data:
            logger.error("No se pudieron extraer datos. Abortando proceso ETL.")
            return False
        
        # FASE 2: TRANSFORMACIÓN
        logger.info("\n[FASE 2/3] TRANSFORMACIÓN DE DATOS")
        transformer = DataTransformer()
        clean_data = transformer.transform_all(raw_data)
        
        # FASE 3: CARGA
        logger.info("\n[FASE 3/3] CARGA DE DATOS")
        loader = DataLoader(
            processed_dir="data/processed",
            analytics_dir="data/analytics"
        )
        
        # Guardar datos procesados
        loader.save_processed(clean_data)
        
        # Crear y guardar tablas analíticas
        analytics = loader.create_analytics_tables(clean_data)
        loader.save_analytics(analytics)
        
        # RESUMEN FINAL
        logger.info("\n" + "=" * 80)
        logger.info("PROCESO ETL COMPLETADO EXITOSAMENTE")
        logger.info("=" * 80)
        logger.info(f"✓ Datasets procesados: {len(clean_data)}")
        logger.info(f"✓ Tablas analíticas creadas: {len(analytics)}")
        logger.info(f"✓ Datos guardados en: data/processed/")
        logger.info(f"✓ Analíticos guardados en: data/analytics/")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"Error en el proceso ETL: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    success = run_etl()
    sys.exit(0 if success else 1)

# Proyecto ETL Trazamatic

Este proyecto implementa un proceso ETL (Extract, Transform, Load) para la gestión y análisis de datos de clientes y materiales de la empresa Trazamatic.

## Estructura del proyecto

```
.env
licence.md
readme.md
requirements.txt
data/
    processed/
    raw/
        clientes.csv
        detalles_orden.csv
        empleados.csv
        materiales.csv
        ordenes_produccion.csv
        productos.csv
        uso_materiales.csv
notebooks/
    clientes.ipynb
src/
    etl.py
```

## Descripción

- **data/raw/**: Contiene los archivos CSV originales con los datos de clientes, materiales, órdenes y productos.
- **data/processed/**: Carpeta destinada a guardar los datos procesados por el ETL.
- **src/etl.py**: Script principal para ejecutar el proceso ETL.
- **notebooks/clientes.ipynb**: Notebook para análisis exploratorio y visualización de los datos de clientes.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar el proyecto.
- **.env**: Variables de entorno para configuración local.

## Instalación

1. Clona el repositorio.
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno en el archivo `.env` si es necesario.

## Uso

Ejecuta el script ETL desde la terminal:
```sh
python src/etl.py
```

También puedes explorar los datos y resultados en el notebook:
```sh
jupyter notebook notebooks/clientes.ipynb
```

## Licencia

Consulta el archivo [licence.md](licence.md) para más información.

## Autor

Trazamatic - Equipo de
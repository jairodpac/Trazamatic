import pandas as pd
import json

# Load all datasets
datasets = {
    'clientes': pd.read_csv('data/raw/clientes.csv'),
    'ordenes_produccion': pd.read_csv('data/raw/ordenes_produccion.csv'),
    'productos': pd.read_csv('data/raw/productos.csv'),
    'materiales': pd.read_csv('data/raw/materiales.csv'),
    'empleados': pd.read_csv('data/raw/empleados.csv'),
    'detalles_orden': pd.read_csv('data/raw/detalles_orden.csv'),
    'uso_materiales': pd.read_csv('data/raw/uso_materiales.csv')
}

result = {}
for name, df in datasets.items():
    result[name] = {
        'rows': len(df),
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'sample': df.head(2).to_dict('records')
    }

with open('data_structure.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False, default=str)

print("Analysis saved to data_structure.json")

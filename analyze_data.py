import pandas as pd
import os

# Load all datasets
data_dir = 'data/raw'
datasets = {
    'clientes': 'clientes.csv',
    'ordenes_produccion': 'ordenes_produccion.csv',
    'productos': 'productos.csv',
    'materiales': 'materiales.csv',
    'empleados': 'empleados.csv',
    'detalles_orden': 'detalles_orden.csv',
    'uso_materiales': 'uso_materiales.csv'
}

print("=" * 80)
print("ANÁLISIS DE ESTRUCTURA DE DATOS - TRAZAMATIC")
print("=" * 80)

for name, filename in datasets.items():
    filepath = os.path.join(data_dir, filename)
    df = pd.read_csv(filepath)
    
    print(f"\n{'=' * 80}")
    print(f"Dataset: {name.upper()}")
    print(f"{'=' * 80}")
    print(f"Archivo: {filename}")
    print(f"Filas: {len(df):,}")
    print(f"Columnas: {len(df.columns)}")
    print(f"\nEstructura de columnas:")
    print("-" * 80)
    for col in df.columns:
        dtype = df[col].dtype
        nulls = df[col].isnull().sum()
        unique = df[col].nunique()
        print(f"  - {col:30s} | Tipo: {str(dtype):10s} | Nulos: {nulls:5d} | Únicos: {unique:6d}")
    
    print(f"\nPrimeras 3 filas:")
    print("-" * 80)
    print(df.head(3).to_string())

print("\n" + "=" * 80)
print("ANÁLISIS COMPLETADO")
print("=" * 80)

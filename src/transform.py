import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:

    # 1. Convertir fecha
    df['fecha_venta'] = pd.to_datetime(df['fecha_venta'], errors='coerce')

    # 2. Manejo de nulos
    df['metodo_pago'] = df['metodo_pago'].fillna('Desconocido')

    # 3. Normalizar texto
    df['producto'] = df['producto'].str.strip().str.title()
    df['provincia'] = df['provincia'].str.strip().str.title()

    # 4. Crear métrica clave
    df['total_venta'] = df['cantidad'] * df['precio_unitario']

    return df
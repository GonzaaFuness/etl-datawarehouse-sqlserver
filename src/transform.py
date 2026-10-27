import pandas as pd

MAX_CANTIDAD = 100

def transform_data(df: pd.DataFrame):
    """Devuelve (df_validas, df_rechazadas)."""
    df = df.copy()
    filas_origen = len(df)

    # 1. Fechas: el CSV mezcla AAAA-MM-DD y DD/MM/AAAA
    texto = df['fecha_venta'].astype(str).str.strip()
    fecha_iso = pd.to_datetime(texto, format='%Y-%m-%d', errors='coerce')
    fecha_dmy = pd.to_datetime(texto, format='%d/%m/%Y', errors='coerce')
    df['fecha_venta'] = fecha_iso.fillna(fecha_dmy)

    # 2. Normalizar texto
    df['producto'] = df['producto'].str.strip().str.title()
    df['provincia'] = df['provincia'].str.strip().str.title()
    df['metodo_pago'] = df['metodo_pago'].fillna('Desconocido')

    # 3. Convertir numéricos (los vacíos quedan como NaN, NO como 0)
    for col in ['cantidad', 'precio_unitario', 'costo_envio']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Deduplicar por id_transaccion, conservando la copia más completa
    df['_completitud'] = df.notna().sum(axis=1)
    df = df.sort_values(
        ['id_transaccion', '_completitud'],
        ascending=[True, False],
        kind='stable'
    )
    duplicadas = df['id_transaccion'].notna() & df.duplicated('id_transaccion', keep='first')
    print(f"🔁 Duplicados eliminados: {duplicadas.sum()}")
    df = df[~duplicadas].drop(columns='_completitud').sort_index()

    # 5. Reglas de validación: cada fila acumula sus motivos de rechazo
    reglas = {
        'Fecha inválida': df['fecha_venta'].isna(),
        'Producto vacío': df['producto'].isna(),
        'Provincia vacía': df['provincia'].isna(),
        'Vendedor vacío': df['vendedor'].isna(),
        'Cliente vacío': df['cliente_id'].isna(),
        'Cantidad inválida': (
            df['cantidad'].isna() | (df['cantidad'] <= 0) | (df['cantidad'] > MAX_CANTIDAD)
        ),
        'Precio cero o negativo': df['precio_unitario'] <= 0,
    }

    df['motivo_rechazo'] = ''
    for motivo, mascara in reglas.items():
        df.loc[mascara, 'motivo_rechazo'] += motivo + '; '
    df['motivo_rechazo'] = df['motivo_rechazo'].str.rstrip('; ')

    rechazadas = df[df['motivo_rechazo'] != ''].copy()
    validas = df[df['motivo_rechazo'] == ''].drop(columns='motivo_rechazo').copy()

    # 6. Métrica clave: total sin costo de envío (precio vacío -> total vacío)
    validas['total_venta'] = (validas['cantidad'] * validas['precio_unitario']).round(2)

    print(f"📥 Filas en el CSV: {filas_origen}")
    print(f"✅ Filas válidas: {len(validas)}")
    print(f"🚫 Filas rechazadas: {len(rechazadas)}")
    print(f"❔ Válidas con precio vacío (se cargan como NULL): {validas['precio_unitario'].isna().sum()}")

    return validas, rechazadas
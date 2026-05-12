import pyodbc
import math


# 🔌 CONEXIÓN
def get_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-VFCCBT5\\SQLEXPRESS;"
        "DATABASE=DataWarehouseVentas;"
        "Trusted_Connection=yes;"
    )


# 🧼 LIMPIEZA SIMPLE PARA DIMENSIONES
def get_unique_values(series):
    return (
        series
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )


# 🧮 LIMPIEZA ROBUSTA PARA NUMÉRICOS (CLAVE)
def safe_float(value):
    try:
        if value is None:
            return 0.0

        if isinstance(value, str) and value.strip() == "":
            return 0.0

        val = float(value)

        if math.isnan(val):
            return 0.0

        return val
    except:
        return 0.0


# 🍷 DIM PRODUCTO
def load_dim_producto(df, conn):
    cursor = conn.cursor()
    productos = get_unique_values(df['producto'])

    for p in productos:
        cursor.execute(
            "IF NOT EXISTS (SELECT 1 FROM dim_producto WHERE nombre_producto = ?) "
            "INSERT INTO dim_producto (nombre_producto) VALUES (?)",
            p, p
        )

    conn.commit()


# 📍 DIM PROVINCIA
def load_dim_provincia(df, conn):
    cursor = conn.cursor()
    provincias = get_unique_values(df['provincia'])

    for p in provincias:
        cursor.execute(
            "IF NOT EXISTS (SELECT 1 FROM dim_provincia WHERE nombre_provincia = ?) "
            "INSERT INTO dim_provincia (nombre_provincia) VALUES (?)",
            p, p
        )

    conn.commit()


# 💳 DIM MÉTODO DE PAGO
def load_dim_metodo_pago(df, conn):
    cursor = conn.cursor()
    metodos = get_unique_values(df['metodo_pago'])

    for m in metodos:
        cursor.execute(
            "IF NOT EXISTS (SELECT 1 FROM dim_metodo_pago WHERE descripcion = ?) "
            "INSERT INTO dim_metodo_pago (descripcion) VALUES (?)",
            m, m
        )

    conn.commit()


# 🧑‍💼 DIM VENDEDOR
def load_dim_vendedor(df, conn):
    cursor = conn.cursor()
    vendedores = get_unique_values(df['vendedor'])

    for v in vendedores:
        cursor.execute(
            "IF NOT EXISTS (SELECT 1 FROM dim_vendedor WHERE nombre_vendedor = ?) "
            "INSERT INTO dim_vendedor (nombre_vendedor) VALUES (?)",
            v, v
        )

    conn.commit()


# 👤 DIM CLIENTE
def load_dim_cliente(df, conn):
    cursor = conn.cursor()
    clientes = get_unique_values(df['cliente_id'])

    for c in clientes:
        cursor.execute(
            "IF NOT EXISTS (SELECT 1 FROM dim_cliente WHERE cliente_id = ?) "
            "INSERT INTO dim_cliente (cliente_id) VALUES (?)",
            c, c
        )

    conn.commit()


# 📅 DIM TIEMPO
def load_dim_tiempo(df, conn):
    cursor = conn.cursor()

    fechas = df['fecha_venta'].dropna().unique()

    for f in fechas:
        fecha_id = int(f.strftime("%Y%m%d"))

        cursor.execute(
            "IF NOT EXISTS (SELECT 1 FROM dim_tiempo WHERE fecha_id = ?) "
            "INSERT INTO dim_tiempo (fecha_id, fecha, anio, mes, dia) VALUES (?, ?, ?, ?, ?)",
            fecha_id, fecha_id, f, f.year, f.month, f.day
        )

    conn.commit()


# 📊 FACT VENTAS (VERSIÓN FINAL)
def load_fact_ventas(df, conn):
    cursor = conn.cursor()

    for _, row in df.iterrows():

        # 🚨 SALTAR FILAS SIN FECHA
        if row['fecha_venta'] is None or str(row['fecha_venta']) == "NaT":
            continue

        cantidad = safe_float(row['cantidad'])
        precio = safe_float(row['precio_unitario'])
        envio = safe_float(row['costo_envio'])

        fecha_id = int(row['fecha_venta'].strftime("%Y%m%d"))

        cursor.execute("""
            INSERT INTO fact_ventas (
                producto_id,
                provincia_id,
                metodo_pago_id,
                vendedor_id,
                cliente_id,
                fecha_id,
                cantidad,
                precio_unitario,
                costo_envio
            )
            SELECT
                dp.producto_id,
                dpr.provincia_id,
                dmp.metodo_pago_id,
                dv.vendedor_id,
                dc.cliente_id,
                dt.fecha_id,
                ?, ?, ?
            FROM dim_producto dp
            JOIN dim_provincia dpr ON dpr.nombre_provincia = ?
            JOIN dim_metodo_pago dmp ON dmp.descripcion = ?
            JOIN dim_vendedor dv ON dv.nombre_vendedor = ?
            JOIN dim_cliente dc ON dc.cliente_id = ?
            JOIN dim_tiempo dt ON dt.fecha_id = ?
            WHERE dp.nombre_producto = ?
        """,
        cantidad,
        precio,
        envio,
        str(row['provincia']).strip(),
        str(row['metodo_pago']).strip(),
        str(row['vendedor']).strip(),
        str(row['cliente_id']).strip(),
        fecha_id,
        str(row['producto']).strip()
        )

    conn.commit()
    print("✅ Fact table cargada")
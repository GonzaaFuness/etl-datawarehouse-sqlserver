from src.extract import extract_data
from src.transform import transform_data
from src.load import (
    get_connection,
    load_dim_producto,
    load_dim_provincia,
    load_dim_metodo_pago,
    load_dim_vendedor,
    load_dim_cliente,
    load_dim_tiempo,
    load_fact_ventas   # 👈 AGREGAR ESTO
)

if __name__ == "__main__":
    df = extract_data("data/raw/dataset_raw_ingenieria_datos.csv")
    df = transform_data(df)

    conn = get_connection()

    load_dim_producto(df, conn)
    load_dim_provincia(df, conn)
    load_dim_metodo_pago(df, conn)
    load_dim_vendedor(df, conn)
    load_dim_cliente(df, conn)
    load_dim_tiempo(df, conn)

    print("✅ Dimensiones cargadas")

    
    load_fact_ventas(df, conn)
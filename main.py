from pathlib import Path

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
    load_fact_ventas
)

if __name__ == "__main__":
    df = extract_data("data/raw/dataset_raw_ingenieria_datos.csv")
    df_validas, df_rechazadas = transform_data(df)

    # Guardar las filas rechazadas para poder auditarlas
    Path("data/rejected").mkdir(parents=True, exist_ok=True)
    df_rechazadas.to_csv(
        "data/rejected/ventas_rechazadas.csv",
        index=False,
        encoding="utf-8-sig"
    )
    print("📄 Rechazadas guardadas en data/rejected/ventas_rechazadas.csv")

    conn = get_connection()

    load_dim_producto(df_validas, conn)
    load_dim_provincia(df_validas, conn)
    load_dim_metodo_pago(df_validas, conn)
    load_dim_vendedor(df_validas, conn)
    load_dim_cliente(df_validas, conn)
    load_dim_tiempo(df_validas, conn)

    print("✅ Dimensiones cargadas")

    load_fact_ventas(df_validas, conn)

    conn.close()
CREATE DATABASE DataWarehouseVentas;
GO

USE DataWarehouseVentas;
GO

CREATE TABLE dim_producto (
    producto_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL
);

CREATE TABLE dim_provincia (
    provincia_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_provincia VARCHAR(100) NOT NULL
);

CREATE TABLE dim_metodo_pago (
    metodo_pago_id INT IDENTITY(1,1) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE dim_vendedor (
    vendedor_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_vendedor VARCHAR(100) NOT NULL
);

CREATE TABLE dim_cliente (
    cliente_id VARCHAR(50) PRIMARY KEY
);

CREATE TABLE dim_tiempo (
    fecha_id INT PRIMARY KEY,
    fecha DATE NOT NULL,
    anio INT NOT NULL,
    mes INT NOT NULL,
    dia INT NOT NULL
);

CREATE TABLE fact_ventas (
    venta_id INT IDENTITY(1,1) PRIMARY KEY,

    producto_id INT NOT NULL,
    provincia_id INT NOT NULL,
    metodo_pago_id INT NOT NULL,
    vendedor_id INT NOT NULL,
    cliente_id VARCHAR(50) NOT NULL,
    fecha_id INT NOT NULL,

    cantidad FLOAT,
    precio_unitario FLOAT,
    costo_envio FLOAT,

    FOREIGN KEY (producto_id)
        REFERENCES dim_producto(producto_id),

    FOREIGN KEY (provincia_id)
        REFERENCES dim_provincia(provincia_id),

    FOREIGN KEY (metodo_pago_id)
        REFERENCES dim_metodo_pago(metodo_pago_id),

    FOREIGN KEY (vendedor_id)
        REFERENCES dim_vendedor(vendedor_id),

    FOREIGN KEY (cliente_id)
        REFERENCES dim_cliente(cliente_id),

    FOREIGN KEY (fecha_id)
        REFERENCES dim_tiempo(fecha_id)
);
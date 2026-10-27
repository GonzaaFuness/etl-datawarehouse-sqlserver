# ETL Data Warehouse con Python y SQL Server

Proyecto de Ingeniería de Datos que implementa un proceso **ETL (Extract, Transform, Load)** para cargar información de ventas desde un archivo CSV hacia un **Data Warehouse** en SQL Server utilizando Python.

---

## Objetivo
Desarrollar un pipeline ETL que permita:

- Extraer datos desde un archivo CSV.
- Limpiar, validar y transformar la información.
- Construir un modelo dimensional.
- Cargar dimensiones y tabla de hechos en SQL Server.
- Guardar las filas rechazadas para poder auditarlas.

Este proyecto fue desarrollado con fines de aprendizaje y para demostrar habilidades orientadas al rol de **Data Engineer Junior**.

---

## Arquitectura
```
CSV
 │
 ▼
Extract
 │
 ▼
Transform ──► data/rejected/ventas_rechazadas.csv
 │
 ▼
Data Warehouse (Modelo Estrella)
 │
 ├── dim_cliente
 ├── dim_producto
 ├── dim_vendedor
 ├── dim_provincia
 ├── dim_metodo_pago
 ├── dim_tiempo
 └── fact_ventas
```
---

## Tecnologías utilizadas
- Python 3
- Pandas
- SQL Server
- PyODBC
- Git
- GitHub
- Visual Studio Code

---

## Estructura del proyecto
```
etl-datawarehouse-sqlserver/
│
├── data/
│   ├── raw/            # CSV de origen
│   └── rejected/       # filas rechazadas (se genera al ejecutar)
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── sql/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
---

## Flujo ETL

### Extract
- Lectura del archivo CSV.
- Carga de datos con Pandas.

### Transform
- **Fechas**: el origen mezcla los formatos `AAAA-MM-DD` y `DD/MM/AAAA`; se parsean ambos con formatos explícitos.
- **Normalización**: limpieza de espacios y capitalización en productos y provincias; método de pago vacío se reemplaza por `Desconocido`.
- **Duplicados**: se eliminan por `id_transaccion`, conservando la copia más completa.
- **Validación**: no se cargan las filas con fecha, producto, provincia, vendedor o cliente vacíos, cantidad menor o igual a 0 o mayor a 100, ni precio menor o igual a 0. Se guardan en `data/rejected/ventas_rechazadas.csv` con el motivo del rechazo.
- **Datos faltantes**: un precio vacío se carga como `NULL`, nunca como 0, para no distorsionar promedios ni totales.
- **Métrica**: `total_venta = cantidad * precio_unitario`. El costo de envío se mantiene en su propia columna.

### Load

Inserción de información en SQL Server.

Se cargan las siguientes tablas:

- dim_producto
- dim_cliente
- dim_vendedor
- dim_provincia
- dim_metodo_pago
- dim_tiempo
- fact_ventas

Detalles de la carga:

- Las dimensiones usan `IF NOT EXISTS`, por lo que se pueden recargar sin duplicar.
- `fact_ventas` se vacía y se recarga dentro de una transacción: si algo falla se hace rollback y no queda una carga a medias.
- Al finalizar se informa cuántas filas se insertaron y cuántas no coincidieron con alguna dimensión.

---

## Modelo de datos
El Data Warehouse utiliza un **Modelo Estrella**, compuesto por una tabla de hechos y seis dimensiones. Todas las dimensiones tienen clave primaria y la tabla de hechos tiene una clave foránea hacia cada una.

```
             dim_cliente
                  │
dim_producto ─ fact_ventas ─ dim_vendedor
                  │
          dim_metodo_pago
                  │
             dim_provincia
                  │
              dim_tiempo
```

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/GonzaaFuness/etl-datawarehouse-sqlserver.git
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar SQL Server

Crear la base de datos `DataWarehouseVentas` con sus tablas y actualizar la cadena de conexión en `src/load.py`.

### 4. Ejecutar
```bash
python main.py
```
---

## Resultados
Sobre el dataset de ejemplo:

| Etapa | Filas |
|---|---|
| CSV de origen | 2550 |
| Duplicados eliminados | 50 |
| Rechazadas por validación | 79 |
| Cargadas en `fact_ventas` | 2421 |

De las filas cargadas, 75 tienen el precio vacío en el origen y se almacenan como `NULL`.

---

## Próximas mejoras
- Implementar PySpark para procesamiento distribuido.
- Agregar Docker.
- Incorporar Airflow para orquestación.
- Implementar logging en lugar de `print`.
- Añadir pruebas unitarias para las reglas de validación.
- Configuración mediante variables de entorno (hoy la conexión está en el código).
- Carga por lotes en lugar de `INSERT` fila por fila.
- Usar `DECIMAL` en lugar de `FLOAT` para los montos.
- Agregar atributos descriptivos a `dim_cliente`.
- Integración con AWS o GCP.

---

## Autor

**Gonzalo Funes**

- [LinkedIn](https://www.linkedin.com/in/gonzalo-funes-439958171/)
- [GitHub](https://github.com/GonzaaFuness)
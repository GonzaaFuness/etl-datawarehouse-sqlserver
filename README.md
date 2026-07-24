# ETL Data Warehouse con Python y SQL Server

Proyecto de Ingeniería de Datos que implementa un proceso **ETL (Extract, Transform, Load)** para cargar información de ventas desde un archivo CSV hacia un **Data Warehouse** en SQL Server utilizando Python.

---

## Objetivo
Desarrollar un pipeline ETL que permita:

- Extraer datos desde un archivo CSV.
- Limpiar y transformar la información.
- Construir un modelo dimensional.
- Cargar dimensiones y tabla de hechos en SQL Server.

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
Transform
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
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
│
├── sql/
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
- Limpieza de registros.
- Eliminación de duplicados.
- Conversión de tipos de datos.
- Normalización de columnas.
- Preparación de tablas dimensionales.

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

---

## Modelo de datos
El Data Warehouse utiliza un **Modelo Estrella**, compuesto por una tabla de hechos y seis dimensiones.

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

Crear la base de datos correspondiente y actualizar la cadena de conexión en `load.py`.

### 4. Ejecutar
```bash
python src/main.py
```
---}
## Resultados
El proceso ETL:

- Extrae datos desde el archivo fuente.
- Realiza transformaciones y limpieza.
- Construye las dimensiones.
- Carga correctamente el Data Warehouse.

---

## Próximas mejoras
- Implementar PySpark para procesamiento distribuido.
- Agregar Docker.
- Incorporar Airflow para orquestación.
- Implementar logging.
- Añadir pruebas unitarias.
- Configuración mediante variables de entorno.
- Integración con AWS o GCP.

---

## Autor

**Gonzalo Funes**

- LinkedIn
- GitHub

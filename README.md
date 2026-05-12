# 📊 ETL Pipeline + Data Warehouse

## 🚀 Descripción

Proyecto de ingeniería de datos desarrollado en Python para procesar datos de ventas y cargarlos en un modelo dimensional en SQL Server.

---

## 🧱 Arquitectura

Pipeline ETL:

1. Extract → CSV
2. Transform → limpieza y transformación con pandas
3. Load → SQL Server

Modelo utilizado:
- Star Schema
- Fact table + dimensiones

---

## ⚙️ Tecnologías

- Python
- Pandas
- SQL Server
- pyodbc
- Git / GitHub

---

## 📂 Estructura del proyecto

```plaintext
src/
  extract.py
  transform.py
  load.py
main.py
```

---

## 🔥 Funcionalidades

- Limpieza de datos
- Manejo de NaN y fechas inválidas
- Modelo dimensional
- Integración Python + SQL Server
- Queries analíticas

---

## ▶️ Ejecución

```bash
pip install -r requirements.txt
python main.py
```

---

## 📊 Ejemplos de análisis

- Ventas totales
- Top productos
- Ventas por mes

---

## 👨‍💻 Autor

Gonzalo Funes
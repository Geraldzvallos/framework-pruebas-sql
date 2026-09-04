# Framework de Pruebas Automáticas SQL

Este proyecto es un framework de pruebas diseñado para ejecutar, validar y auditar sentencias SQL (DML y consultas) contra bases de datos relacionales (Oracle MVP), garantizando el aislamiento transaccional y la trazabilidad de los resultados.

## 🚀 Arquitectura y Tecnologías
*   **Lenguaje:** Python 3.x
*   **API Web:** FastAPI + Uvicorn
*   **ORM y Base de Datos Interna:** SQLAlchemy + SQLite (Escalable a PostgreSQL)
*   **Conector Objetivo:** `oracledb` (Modo Thin)
*   **Patrones de Diseño:** Strategy (Motor de Validación), Repository (Gestión de estado interno).

## ⚙️ Estructura del Proyecto
El código sigue una arquitectura de capas desacopladas:
*   `/api`: Controladores y definición de endpoints (FastAPI Routers).
*   `/core`: Configuraciones globales y conexión a la base de datos interna.
*   `/engine`: Lógica dura del framework (TargetDatabaseExecutor y ValidationContext).
*   `/models`: Esquemas de Pydantic y Modelos ORM de SQLAlchemy.

## 🛠️ Instrucciones de Instalación

1. **Clonar el repositorio y entrar a la carpeta:**
   ```bash
   git clone <url-del-repositorio>
   cd framework_pruebas_sql
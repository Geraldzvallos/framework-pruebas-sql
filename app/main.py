from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import test_case
from app.models import history
from app.models import suite  
from app.api import test_cases
from app.api import executions
from app.api import suites  # 1. Importamos las rutas de suites

# Creamos las tablas en SQLite (ahora creará test_cases y execution_history)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Framework de Pruebas SQL",
    description="API para ejecución y validación de pruebas en bases de datos relacionales.",
    version="1.0.0"
)

app.include_router(test_cases.router, prefix="/api", tags=["Casos de Prueba"])
app.include_router(executions.router, prefix="/api", tags=["Motor de Ejecución"]) # 2. Lo conectamos
app.include_router(suites.router, prefix="/api", tags=["Suites de Pruebas"]) # 2. Lo conectamos

@app.get("/")
def read_root():
    return {"status": "ok", "message": "El motor del Framework SQL está en línea."}
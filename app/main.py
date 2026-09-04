from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import test_case
from app.api import test_cases
from app.api import executions # 1. Importamos el nuevo módulo

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Framework de Pruebas SQL",
    description="API para ejecución y validación de pruebas en bases de datos relacionales.",
    version="1.0.0"
)

app.include_router(test_cases.router, prefix="/api", tags=["Casos de Prueba"])
app.include_router(executions.router, prefix="/api", tags=["Motor de Ejecución"]) # 2. Lo conectamos

@app.get("/")
def read_root():
    return {"status": "ok", "message": "El motor del Framework SQL está en línea."}
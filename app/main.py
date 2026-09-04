from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.core.database import engine, Base
from app.models import test_case
from app.models import history
from app.models import suite
from app.api import test_cases
from app.api import executions
from app.api import suites

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Framework de Pruebas SQL",
    description="API para ejecución y validación de pruebas en bases de datos relacionales.",
    version="1.0.0"
)

# --- CONFIGURACIÓN CORS (Permite que tu frontend HTML se conecte) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se pone el dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------------------------

app.include_router(test_cases.router, prefix="/api", tags=["Casos de Prueba"])
app.include_router(executions.router, prefix="/api", tags=["Motor de Ejecución"])
app.include_router(suites.router, prefix="/api", tags=["Suites de Pruebas"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "El motor del Framework SQL está en línea."}
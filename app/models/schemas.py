from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, List

# --- ESQUEMAS DE CASOS DE PRUEBA ---

class TestCaseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    sql_query: str
    expected_result: str

class TestCaseResponse(TestCaseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- ESQUEMAS DEL MOTOR DE EJECUCIÓN SQL ---

class ExecutionRequest(BaseModel):
    """Payload requerido para aislar y probar una ejecución SQL contra el SGBD objetivo."""
    dsn: str
    user: str
    password: str
    sql_query: str

class ExecutionResponse(BaseModel):
    """Estructura de respuesta estandarizada para operaciones del motor SQL."""
    success: bool
    data: List[Any]
    message: str
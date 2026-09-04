from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, List
from datetime import datetime  # <-- Importación correctamente ubicada al inicio

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


# --- ESQUEMAS DEL HISTORIAL DE EJECUCIONES ---

class HistoryResponse(BaseModel):
    """Esquema para devolver la evidencia de una ejecución guardada."""
    id: int
    test_case_id: Optional[int]
    status: str
    executed_at: datetime
    duration_ms: float
    executed_sql: str
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# --- ESQUEMAS DE SUITES DE PRUEBAS ---

class TestSuiteCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TestSuiteResponse(TestSuiteCreate):
    id: int
    # Permite devolver la Suite con todos sus Casos de Prueba anidados
    test_cases: List[TestCaseResponse] = [] 
    
    model_config = ConfigDict(from_attributes=True)

class SuiteExecutionSummary(BaseModel):
    """Reporte consolidado tras ejecutar una Suite de pruebas completa."""
    suite_id: int
    suite_name: str
    total_tests: int
    passed: int
    failed: int
    errors: int
    total_duration_ms: float
    details: List[HistoryResponse] = []
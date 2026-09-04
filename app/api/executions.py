from fastapi import APIRouter, HTTPException
from app.models.schemas import ExecutionRequest, ExecutionResponse
from app.engine.executor import TargetDatabaseExecutor

router = APIRouter()

@router.post("/execute/", response_model=ExecutionResponse)
def execute_target_sql(request: ExecutionRequest):
    """
    Instancia el motor de base de datos, ejecuta la sentencia SQL de prueba 
    y garantiza el cierre de la conexión sin importar el resultado.
    """
    executor = TargetDatabaseExecutor(
        dsn=request.dsn, 
        user=request.user, 
        password=request.password
    )
    
    try:
        success, data, message = executor.execute_query(request.sql_query)
        if not success:
            raise HTTPException(status_code=400, detail=message)
            
        return ExecutionResponse(success=success, data=data, message=message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del motor: {str(e)}")
        
    finally:
        executor.disconnect()
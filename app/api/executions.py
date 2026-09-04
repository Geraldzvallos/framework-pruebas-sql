import time
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import schemas
from app.models import test_case as models_tc
from app.models import history as models_history
from app.models import suite as models_suite # <-- NUEVA LÍNEA
from app.engine.executor import TargetDatabaseExecutor
from app.engine.validator import ValidationContext, RowCountValidation

router = APIRouter()

@router.post("/execute/raw", response_model=schemas.ExecutionResponse)
def execute_target_sql(request: schemas.ExecutionRequest):
    """Ejecuta una sentencia SQL aislada sin validación (Prueba de conexión/Sintaxis)."""
    executor = TargetDatabaseExecutor(
        dsn=request.dsn, user=request.user, password=request.password
    )
    try:
        success, data, message = executor.execute_query(request.sql_query)
        if not success:
            raise HTTPException(status_code=400, detail=message)
        return schemas.ExecutionResponse(success=success, data=data, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        executor.disconnect()

@router.post("/execute/test-case/{test_case_id}", response_model=schemas.HistoryResponse)
def run_test_case(test_case_id: int, db_credentials: schemas.ExecutionRequest, db: Session = Depends(get_db)):
    """
    Orquestador Principal: Recupera un caso de prueba, lo ejecuta en Oracle, 
    valida el resultado y registra la evidencia en el historial.
    """
    # 1. Buscar el caso de prueba en nuestra BD interna
    tc = db.query(models_tc.TestCase).filter(models_tc.TestCase.id == test_case_id).first()
    if not tc:
        raise HTTPException(status_code=404, detail="Caso de prueba no encontrado.")

    # Variables para la auditoría
    start_time = time.time()
    status = "ERROR"
    error_msg = None
    execution_data = []

    # 2. Ejecutar contra Oracle
    executor = TargetDatabaseExecutor(
        dsn=db_credentials.dsn, user=db_credentials.user, password=db_credentials.password
    )
    
    try:
        success, execution_data, db_msg = executor.execute_query(tc.sql_query)
        if not success:
            error_msg = db_msg
        else:
            # 3. Validar el resultado (Por defecto, validamos cantidad de filas para el MVP)
            # Instanciamos el patrón Strategy
            validator = ValidationContext(RowCountValidation())
            is_valid = validator.execute_validation(execution_data, tc.expected_result)
            status = "PASS" if is_valid else "FAIL"

    except Exception as e:
        error_msg = str(e)
    finally:
        executor.disconnect()

    # 4. Registrar en el historial de forma permanente
    duration_ms = round((time.time() - start_time) * 1000, 2)
    
    history_record = models_history.ExecutionHistory(
        test_case_id=tc.id,
        status=status,
        duration_ms=duration_ms,
        executed_sql=tc.sql_query,
        error_message=error_msg
    )
    db.add(history_record)
    db.commit()
    db.refresh(history_record)

    return history_record

@router.post("/execute/suite/{suite_id}", response_model=schemas.SuiteExecutionSummary)
def run_test_suite(suite_id: int, db_credentials: schemas.ExecutionRequest, db: Session = Depends(get_db)):
    """
    Ejecuta en ráfaga todos los casos de prueba asociados a una Suite 
    usando una conexión única, y devuelve un reporte consolidado.
    """
    # 1. Buscamos la suite y sus casos asociados
    suite = db.query(models_suite.TestSuite).filter(models_suite.TestSuite.id == suite_id).first()
    if not suite:
        raise HTTPException(status_code=404, detail="Suite no encontrada.")

    # 2. Inicializamos el reporte gerencial
    summary = schemas.SuiteExecutionSummary(
        suite_id=suite.id,
        suite_name=suite.name,
        total_tests=len(suite.test_cases),
        passed=0, failed=0, errors=0, total_duration_ms=0.0
    )

    if summary.total_tests == 0:
        return summary # Retornamos de inmediato si la suite está vacía

    # 3. Abrimos UNA SOLA conexión a la base de datos objetivo
    executor = TargetDatabaseExecutor(
        dsn=db_credentials.dsn, user=db_credentials.user, password=db_credentials.password
    )
    
    try:
        # 4. Iteramos y ejecutamos cada caso de prueba
        for tc in suite.test_cases:
            start_time = time.time()
            status = "ERROR"
            error_msg = None
            
            success, execution_data, db_msg = executor.execute_query(tc.sql_query)
            
            if not success:
                error_msg = db_msg
            else:
                validator = ValidationContext(RowCountValidation())
                is_valid = validator.execute_validation(execution_data, tc.expected_result)
                status = "PASS" if is_valid else "FAIL"
            
            duration_ms = round((time.time() - start_time) * 1000, 2)
            summary.total_duration_ms += duration_ms
            
            # Contadores para el reporte
            if status == "PASS": summary.passed += 1
            elif status == "FAIL": summary.failed += 1
            else: summary.errors += 1
            
            # Guardamos la evidencia en el historial
            history_record = models_history.ExecutionHistory(
                test_case_id=tc.id,
                status=status,
                duration_ms=duration_ms,
                executed_sql=tc.sql_query,
                error_message=error_msg
            )
            db.add(history_record)
            db.commit()
            db.refresh(history_record)
            
            summary.details.append(history_record)
            
    finally:
        # Garantizamos que la conexión a Oracle se cierre pase lo que pase
        executor.disconnect()

    summary.total_duration_ms = round(summary.total_duration_ms, 2)
    return summary
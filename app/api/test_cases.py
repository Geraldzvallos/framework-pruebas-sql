from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import test_case as models
from app.models import schemas

# Creamos un enrutador para agrupar estas rutas
router = APIRouter()

# Endpoint para CREAR un caso de prueba
@router.post("/test-cases/", response_model=schemas.TestCaseResponse)
def create_test_case(test_case: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    # Convertimos los datos validados de Pydantic al modelo de base de datos
    db_test_case = models.TestCase(**test_case.model_dump())
    
    db.add(db_test_case)    # Lo preparamos para guardar
    db.commit()             # Guardamos físicamente en SQLite
    db.refresh(db_test_case) # Refrescamos para obtener el ID que generó la base de datos
    
    return db_test_case

# Endpoint para LEER todos los casos de prueba guardados
@router.get("/test-cases/", response_model=list[schemas.TestCaseResponse])
def read_test_cases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    test_cases = db.query(models.TestCase).offset(skip).limit(limit).all()
    return test_cases

@router.delete("/test-cases/{test_case_id}", status_code=204)
def delete_test_case(test_case_id: int, db: Session = Depends(get_db)):
    """Elimina un caso de prueba de la base de datos."""
    from app.models.test_case import TestCase # Importación directa y segura
    
    db_tc = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not db_tc:
        raise HTTPException(status_code=404, detail="Caso de prueba no encontrado.")
    
    db.delete(db_tc)
    db.commit()
    return
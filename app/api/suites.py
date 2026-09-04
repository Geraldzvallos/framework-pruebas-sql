from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import suite as models_suite
from app.models import test_case as models_tc
from app.models import schemas

router = APIRouter()

@router.post("/suites/", response_model=schemas.TestSuiteResponse)
def create_suite(suite: schemas.TestSuiteCreate, db: Session = Depends(get_db)):
    """Crea una nueva Suite de Pruebas vacía."""
    db_suite = models_suite.TestSuite(**suite.model_dump())
    db.add(db_suite)
    db.commit()
    db.refresh(db_suite)
    return db_suite

@router.post("/suites/{suite_id}/test-cases/{test_case_id}", response_model=schemas.TestSuiteResponse)
def add_test_case_to_suite(suite_id: int, test_case_id: int, db: Session = Depends(get_db)):
    """Vincula un Caso de Prueba existente a una Suite de Pruebas."""
    db_suite = db.query(models_suite.TestSuite).filter(models_suite.TestSuite.id == suite_id).first()
    db_tc = db.query(models_tc.TestCase).filter(models_tc.TestCase.id == test_case_id).first()
    
    if not db_suite or not db_tc:
        raise HTTPException(status_code=404, detail="Suite o Caso de Prueba no encontrado.")
        
    # Magia del ORM: agregamos el caso a la lista y SQLAlchemy arma la relación
    db_suite.test_cases.append(db_tc)
    db.commit()
    db.refresh(db_suite)
    
    return db_suite
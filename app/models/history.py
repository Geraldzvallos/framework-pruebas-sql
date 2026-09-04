"""
Modelo de base de datos para registrar la trazabilidad de las ejecuciones.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from datetime import datetime
from app.core.database import Base

class ExecutionHistory(Base):
    __tablename__ = "execution_history"

    id = Column(Integer, primary_key=True, index=True)
    
    # Llave foránea: relaciona esta ejecución con un caso de prueba específico
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=True)
    
    # Estados permitidos: PASS, FAIL, ERROR
    status = Column(String, index=True, nullable=False) 
    
    # Fecha y hora exacta de la prueba
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    # Rendimiento
    duration_ms = Column(Float, nullable=False)
    
    # Evidencia técnica
    executed_sql = Column(Text, nullable=False)
    error_message = Column(Text, nullable=True)
from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class TestCase(Base):
    __tablename__ = "test_cases"

    # Definimos las columnas de nuestra tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Aquí guardaremos el SELECT, INSERT, UPDATE o DELETE
    sql_query = Column(Text, nullable=False)
    
    # Lo que esperamos que la base de datos nos responda
    expected_result = Column(String, nullable=False)    
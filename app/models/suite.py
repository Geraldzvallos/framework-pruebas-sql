"""
Modelo de base de datos para las Suites de Pruebas.
Permite agrupar múltiples Casos de Prueba para su ejecución en bloque.
"""
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# Tabla de asociación (Muchos a Muchos) entre Suites y Casos de Prueba
suite_test_case_table = Table(
    "suite_test_case",
    Base.metadata,
    Column("suite_id", Integer, ForeignKey("test_suites.id"), primary_key=True),
    Column("test_case_id", Integer, ForeignKey("test_cases.id"), primary_key=True)
)

class TestSuite(Base):
    __tablename__ = "test_suites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Relación con el modelo TestCase
    test_cases = relationship("TestCase", secondary=suite_test_case_table, backref="suites")
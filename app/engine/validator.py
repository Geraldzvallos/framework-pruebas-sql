"""
Módulo de validación para el Framework de Pruebas.
Implementa el Patrón Strategy para evaluar dinámicamente los resultados
de la ejecución SQL contra los criterios esperados.
"""
from abc import ABC, abstractmethod
from typing import Any, List

class ValidationStrategy(ABC):
    """Interfaz base que define el contrato para cualquier regla de validación."""
    
    @abstractmethod
    def evaluate(self, execution_data: List[Any], expected_value: str) -> bool:
        """
        Evalúa el resultado de la base de datos contra el valor esperado.
        
        Args:
            execution_data: Lista de resultados devueltos por el executor SQL.
            expected_value: El valor configurado en el caso de prueba.
            
        Returns:
            bool: True si la prueba pasa (PASS), False si falla (FAIL).
        """
        pass


class RowCountValidation(ValidationStrategy):
    """Estrategia para validar la cantidad exacta de filas devueltas."""
    
    def evaluate(self, execution_data: List[Any], expected_value: str) -> bool:
        try:
            expected_count = int(expected_value.strip())
            return len(execution_data) == expected_count
        except ValueError:
            return False


class ExistenceValidation(ValidationStrategy):
    """Estrategia para validar si la consulta devolvió al menos un registro."""
    
    def evaluate(self, execution_data: List[Any], expected_value: str) -> bool:
        # Si expected_value es "TRUE", verificamos que haya data. Si es "FALSE", verificamos que esté vacío.
        expect_exists = expected_value.strip().upper() == "TRUE"
        has_data = len(execution_data) > 0
        return has_data == expect_exists


class ValidationContext:
    """
    Contexto principal que recibe la data de ejecución y delega la evaluación
    a la estrategia inyectada en tiempo de ejecución.
    """
    
    def __init__(self, strategy: ValidationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ValidationStrategy) -> None:
        """Permite cambiar la estrategia de validación dinámicamente."""
        self._strategy = strategy

    def execute_validation(self, execution_data: List[Any], expected_value: str) -> bool:
        """Ejecuta la evaluación utilizando la estrategia actual."""
        return self._strategy.evaluate(execution_data, expected_value)
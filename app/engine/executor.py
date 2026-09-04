"""
Módulo de ejecución SQL para el Framework de Pruebas.
Gestiona la conectividad y el aislamiento transaccional sobre SGBDs relacionales.
"""
import oracledb
from typing import Any, Dict, List, Tuple, Optional

class TargetDatabaseExecutor:
    """
    Administra la sesión con la base de datos objetivo (Oracle) garantizando 
    el cumplimiento de las restricciones de seguridad (ej. Rollback por defecto).
    """
    
    def __init__(self, dsn: str, user: str, password: str):
        self.dsn = dsn
        self.user = user
        self.password = password
        self._connection: Optional[oracledb.Connection] = None

    def connect(self) -> None:
        """Establece la conexión utilizando oracledb en modo thin."""
        self._connection = oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn
        )
        self._connection.autocommit = False

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[Any], str]:
        """
        Ejecuta una sentencia SQL aislada.
        
        Args:
            query: Sentencia SQL a procesar.
            params: Diccionario de parámetros para binding seguro.
            
        Returns:
            Tuple[bool, List[Any], str]: 
                - bool: Indicador de éxito (True) o fallo (False).
                - List: Filas recuperadas (SELECT) o lista vacía (DML).
                - str: Mensaje técnico del estado de la transacción.
        """
        if not self._connection:
            self.connect()

        cursor = self._connection.cursor()
        try:
            cursor.execute(query, params or {})
            
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                return True, result, "Ejecución exitosa."
            
            rowcount = cursor.rowcount
            
            # Control transaccional exigido en la especificación
            self._connection.rollback()
            
            return True, [], f"DML procesado. {rowcount} filas afectadas. Rollback aplicado."

        except oracledb.Error as e:
            error_obj, = e.args
            return False, [], f"ORA-{error_obj.code}: {error_obj.message}"
            
        finally:
            cursor.close()

    def disconnect(self) -> None:
        """Libera los recursos de conexión activos."""
        if self._connection:
            self._connection.close()
            self._connection = None
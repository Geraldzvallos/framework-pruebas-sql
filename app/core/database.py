from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de nuestra base de datos interna local (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./framework_interno.db"

# Creamos el motor de conexión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creamos la fábrica de sesiones para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán todos nuestros modelos (tablas)
Base = declarative_base()

# Inyección de dependencias para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
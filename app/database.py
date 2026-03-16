from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:38291245PP@localhost:5432/marvel_db"

# Motor de conexión
engine = create_engine(DATABASE_URL)

# Sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para los modelos
Base = declarative_base()


# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
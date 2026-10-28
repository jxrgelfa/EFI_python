from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./database.db"

# Para SQLite es necesario check_same_thread=False en aplicaciones multi-hilo como FastAPI
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def init_db() -> None:
    """Crea las tablas en la base de datos si no existen."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Inyector de dependencias para obtener una sesión de base de datos."""
    with Session(engine) as session:
        yield session

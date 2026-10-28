from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import init_db
from src.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización de base de datos / tablas
    init_db()
    yield


app = FastAPI(
    title="EFI Python API",
    description="API desarrollada para la Evaluación Final Integradora",
    version="0.1.0",
    lifespan=lifespan,
)

# Registro de routers
app.include_router(health.router)


@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de EFI",
        "docs": "/docs",
    }

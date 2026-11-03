from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqlmodel import SQLModel

from database import engine

# Importar modelos para que SQLModel los registre antes de crear las tablas
from models import marca, pedido, productos, usuario  # noqa: F401

from routers.marca import marca_router
from routers.pedido import pedido_router
from routers.productos import productos_router
from routers.usuario import usuario_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas en la base de datos al iniciar la API
    SQLModel.metadata.create_all(engine)
    yield


# Inicio de setup de la API
app = FastAPI(
    title="EFI Python API",
    description="API desarrollada para la EFI",
    version="0.1.0",
    lifespan=lifespan,
)


# Routers
app.include_router(marca_router, tags=["Marcas"], prefix="/marcas")
app.include_router(pedido_router, tags=["Pedidos"], prefix="/pedidos")
app.include_router(productos_router, tags=["Productos"], prefix="/productos")
app.include_router(usuario_router, tags=["Usuarios"], prefix="/usuarios")

# Paginacion de los resultados de la App
add_pagination(app)

# Acceso del CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir="src")

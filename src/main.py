from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from routers.marca import marca_router
from routers.pedido import pedido_router
from routers.productos import productos_router
from routers.usuario import usuario_router
from contextlib import asynccontextmanager
from pathlib import Path
from alembic.config import Config
from alembic import command


BASE_DIR = Path(__file__).resolve().parent.parent


def run_migrations():
    ini_path = BASE_DIR / "alembic.ini"
    alembic_dir = BASE_DIR / "alembic"

    # Verificación rápida en los logs para confirmar que se subieron los archivos
    if not ini_path.exists():
        raise FileNotFoundError(f"No se encontró alembic.ini en: {ini_path}")

    alembic_cfg = Config(str(ini_path))

    # Forzamos la ruta absoluta de la carpeta de migraciones
    alembic_cfg.set_main_option("script_location", str(alembic_dir))

    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


#Inicio de setup de la API

app = FastAPI(lifespan=lifespan)

app.title = "EFI Python API"
app.description = "API Desarrollada como evaluacion final intengradora, con el fin de gestionar una tienda de zapatillas virtual (e-commerce)"
app.version="0.1.0"


#Routers

app.include_router(marca_router, tags=["Marcas"], prefix="/marcas")
app.include_router(pedido_router, tags=["Pedidos"], prefix="/pedidos")
app.include_router(productos_router, tags=["Productos"], prefix="/productos")
app.include_router(usuario_router, tags=["Usuarios"], prefix="/usuarios")

#Paginacion de los resultados de la App
add_pagination(app)

#el acceso del CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "https://sneakerstoreefi.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








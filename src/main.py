from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src.routers.health import health_router
from src.routers.productos import productos_router
from src.routers.usuario import usuarios_router
import src.models

#Inicio de setup de la API
app = FastAPI(
    title="EFI Python API",
    description="API desarrollada para la EFI",
    version="0.1.0",
)



#Routers

app.include_router(health_router, tags=["Salud"], prefix="/health")
app.include_router(productos_router, tags=["Productos"], prefix="/productos")
app.include_router(usuarios_router, tags=["Usuarios"], prefix="/usuarios")

#Paginacion de los resultados de la App
add_pagination(app)

#el acceso del CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)







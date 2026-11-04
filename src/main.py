from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from routers.marca import marca_router
from routers.pedido import pedido_router
from routers.productos import productos_router
from routers.usuario import usuario_router

#Inicio de setup de la API
app = FastAPI(
    title="EFI Python API",
    description="API Desarrollada como evaluacion final intengradora, con el fin de gestionar una tienda de zapatillas virtual (e-commerce)",
    version="0.1.0",
)


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
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








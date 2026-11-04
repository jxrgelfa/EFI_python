EFI - Práctica Profesionalizante I: Python

Docente: Facundo Esteban Lemo
Institución: ITEC Río Cuarto
Carrera: Desarrollo de Software (2026)

Integrantes
Bianchi, Santiago - s.bianchiceli@itecriocuarto.org.ar
Fernandez, Jorge - l.fernandez@itecriocuarto.org.ar
Martoccio, Brisa - b.martoccio@itecriocuarto.org.ar
Sosa, Agustin - o.sosa@itecriocuarto.org.ar

Descripcion del Proyecto

API REST desarrollada con Python, FastAPI y SQLModel, con el objetivo de gestionar un e-commerce de calzado deportivo. El sistema administra entidades vinculadas mediante relaciones de clave foránea y esquemas anidados (Nested):

Marcas: Marcas comerciales asociadas a productos.
Productos: Artículos a la venta vinculados a una marca.
Usuarios: Clientes y gestión de credenciales/autenticación.
Pedidos: Órdenes de compra que relacionan usuarios y productos.

Cuenta con soporte CORS habilitado para comunicarse con el frontend de la EFI de JavaScript, paginación en todos los listados mediante fastapi-pagination y control de versiones de esquema con Alembic.


Tecnologías Utilizadas
FastAPI (fastapi[standard])
SQLModel (Pydantic + SQLAlchemy)
SQLite
Alembic (Migraciones)
FastAPI-Pagination
Uvicorn


Instalación y Puesta en Marcha
1. Clonar el repositorio

git clone https://github.com/jxrgelfa/EFI_python.git
cd EFI_python


. Crear y activar el entorno virtual

# Windows
python -m venv env
.\env\Scripts\activate
# Linux / macOS
python3 -m venv env
source env/bin/activate


3. Instalar las dependencias

pip install -r requirements.txt

Aplicar las migraciones de base de datos

alembic upgrade head

Iniciar la API en modo desarrollo

fastapi dev src/main.py

La aplicación quedará disponible en: http://127.0.0.1:8000.


DOCUMENTACION INTERACTIVA

FastAPI expone la documentación interactiva en:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc



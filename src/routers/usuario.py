from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from database import get_db
from models.anidados import UsuarioNested
from models.usuario import (
    Usuario,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioPublic,
)

usuario_router = APIRouter()

DICT_NOT_FOUND: dict = {
    404: {
        "description": "Usuario no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Usuario no encontrado"
                }
            }
        },
    }
}


# 1. READ ALL (Paginado)
@usuario_router.get("", response_model=Page[UsuarioPublic])
def listar_usuarios(db: Session = Depends(get_db)):
    return paginate(db, select(Usuario))


# 2. READ BY ID (Con pedidos anidados)
@usuario_router.get(
    "/{id}",
    responses=DICT_NOT_FOUND,
    response_model=UsuarioNested,
)
def get_usuario(
    id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")],
    db: Session = Depends(get_db),
):
    usuario = db.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# 3. CREATE (Validando unicidad de email)
@usuario_router.post("", response_model=UsuarioPublic, status_code=201)
def crear_usuario(
    usuario_nuevo: UsuarioCreate,
    db: Session = Depends(get_db),
):
    usuario_existente = db.exec(
        select(Usuario).where(Usuario.email == usuario_nuevo.email)
    ).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    usuario_db = Usuario.model_validate(usuario_nuevo)
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db


# 4. UPDATE
@usuario_router.put(
    "/{id}",
    responses=DICT_NOT_FOUND,
    response_model=UsuarioPublic,
)
def actualizar_usuario(
    id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")],
    usuario_update: UsuarioCreate,
    db: Session = Depends(get_db),
):
    usuario_db = db.get(Usuario, id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Si cambió el email, verificar que no pertenezca a otro usuario
    if usuario_update.email != usuario_db.email:
        email_ocupado = db.exec(
            select(Usuario).where(Usuario.email == usuario_update.email, Usuario.id != id)
        ).first()
        if email_ocupado:
            raise HTTPException(status_code=400, detail="El email ya está registrado por otro usuario")

    usuario_data = usuario_update.model_dump(exclude_unset=True)
    usuario_db.sqlmodel_update(usuario_data)

    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db


# 5. DELETE
@usuario_router.delete(
    "/{id}",
    responses=DICT_NOT_FOUND,
    status_code=204,
)
def eliminar_usuario(
    id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")],
    db: Session = Depends(get_db),
):
    usuario_db = db.get(Usuario, id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario_db)
    db.commit()


# 6. LOGIN (Opcional pero útil para autenticación con UsuarioLogin)
@usuario_router.post("/login", response_model=UsuarioPublic)
def login(
    credenciales: UsuarioLogin,
    db: Session = Depends(get_db),
):
    usuario = db.exec(
        select(Usuario).where(Usuario.email == credenciales.email)
    ).first()
    if not usuario or usuario.contrasena != credenciales.contrasena:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return usuario

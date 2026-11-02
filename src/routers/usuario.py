from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from src.database import get_db
from src.models.usuario import (
    Usuario,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioPublic,
    UsuarioPublicNested,
)

usuarios_router = APIRouter()

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Usuario no encontrado",
        "content": {"application/json": {"example": {"detail": "Usuario no encontrado"}}},
    }
}


# 1. LISTAR USUARIOS (Paginado)
@usuarios_router.get("", response_model=Page[UsuarioPublic])
def listar_usuarios(db: Session = Depends(get_db)):
    return paginate(db, select(Usuario))


# 2. OBTENER USUARIO POR ID (Con sus pedidos asociados)
@usuarios_router.get("/{id}", responses=NOT_FOUND_RESPONSE, response_model=UsuarioPublicNested)
def get_usuario(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    usuario = db.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# 3. CREAR USUARIO (Validando que el email no esté repetido)
@usuarios_router.post("", response_model=UsuarioPublic, status_code=201)
def crear_usuario(usuario_nuevo: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificamos si ya existe un usuario con ese email
    usuario_existente = db.exec(select(Usuario).where(Usuario.email == usuario_nuevo.email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    usuario_db = Usuario.model_validate(usuario_nuevo)
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db


# 4. ACTUALIZAR USUARIO
@usuarios_router.put("/{id}", responses=NOT_FOUND_RESPONSE, response_model=UsuarioPublic)
def actualizar_usuario(
    id: Annotated[int, Path(gt=0)],
    usuario_update: UsuarioCreate,
    db: Session = Depends(get_db),
):
    usuario_db = db.get(Usuario, id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Si cambió el email, chequeamos que no pertenezca a otro usuario
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


# 5. ELIMINAR USUARIO
@usuarios_router.delete("/{id}", responses=NOT_FOUND_RESPONSE, status_code=204)
def eliminar_usuario(id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    usuario = db.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()


# 6. LOGIN SIMPLE (Usando el esquema UsuarioLogin del modelo)
@usuarios_router.post("/login", response_model=UsuarioPublic)
def login(credenciales: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.exec(select(Usuario).where(Usuario.email == credenciales.email)).first()
    if not usuario or usuario.contrasena != credenciales.contrasena:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return usuario



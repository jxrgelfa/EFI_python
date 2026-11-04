from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Depends, Query
from sqlmodel import Session, select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from database import get_db
from models.anidados import ProductoNested
from models.productos import (
    Producto,
    ProductoCreate,
    ProductoPublic,
)

productos_router = APIRouter()

NOT_FOUND_RESPONSE = {
    404: {
        "description": "si el Producto no se encuentra en la lista",
        "content": {
            "application/json": {
                "example": {"detail": "Producto no encontrado"}
            }
        },
    }
}


@productos_router.get("", response_model=Page[ProductoPublic])
def listar_productos(db: Session = Depends(get_db)):
    return paginate(db, select(Producto))


@productos_router.get(
    "/{id}", responses=NOT_FOUND_RESPONSE, response_model=ProductoNested
)
def get_producto(
    id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):
    producto = db.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@productos_router.post("", response_model=ProductoPublic, status_code=201)
def crear_producto(producto_nuevo: ProductoCreate, db: Session = Depends(get_db)):
    producto_creado = Producto.model_validate(producto_nuevo)
    db.add(producto_creado)
    db.commit()
    db.refresh(producto_creado)
    return producto_creado


@productos_router.put(
    "/{id}", responses=NOT_FOUND_RESPONSE, response_model=ProductoPublic
)
def actualizar_producto(
    id: Annotated[int, Path(gt=0)],
    producto_update: ProductoCreate,
    db: Session = Depends(get_db),
):
    producto_db = db.get(Producto, id)
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_data = producto_update.model_dump(exclude_unset=True)
    producto_db.sqlmodel_update(producto_data)

    db.add(producto_db)
    db.commit()
    db.refresh(producto_db)
    return producto_db


@productos_router.delete(
    "/{id}", responses=NOT_FOUND_RESPONSE, status_code=204
)
def eliminar_producto(
    id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):
    producto = db.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()

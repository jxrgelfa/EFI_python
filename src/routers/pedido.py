from typing import Annotated
from fastapi import HTTPException, Path, APIRouter, Depends
from database import get_db
from models.pedido import Pedido, PedidoBase, PedidoCreate, PedidoPublic
from models.anidados import PedidoNested
from sqlmodel import Session, select
from fastapi_pagination import Page, paginate

pedido_router = APIRouter()

DICT_NOT_FOUND: dict = {
    404: {
        "description": "Si el pedido no se encuentra en la lista",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Pedido no encontrado"
                }
            }
        }
    }
}

##########################
# METODOS GET
##########################

@pedido_router.get('/', response_model=Page[PedidoPublic])
async def get_pedidos(db: Session = Depends(get_db)):
    pedidos = db.exec(select(Pedido)).all()
    return paginate(
        pedidos
    )

@pedido_router.get(
    '/{id}',
    responses=DICT_NOT_FOUND,
    response_model=PedidoNested
)
async def get_pedido_id(id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")], db: Session = Depends(get_db)):
    pedido_obtenido = db.get(Pedido, id)
    if not pedido_obtenido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido_obtenido

##########################
# METODO POST 
##########################

@pedido_router.post(
    '/',
    response_model=PedidoPublic,
    status_code=201
)
async def agregar_pedido(nuevo_pedido: PedidoCreate, db: Session = Depends(get_db)):
    pedido_db = Pedido.model_validate(nuevo_pedido)

    db.add(pedido_db)
    db.commit()
    db.refresh(pedido_db)

    return pedido_db

    
##########################
# METODO PUT
##########################

@pedido_router.put(
    '/{id}',
    responses=DICT_NOT_FOUND,
    response_model=PedidoPublic
)
async def actualizar_pedido(
    id: Annotated[int, Path(gt=0)],
    pedido_editar: PedidoCreate,
    db: Session = Depends(get_db)
):

    pedido_obtenido = db.get(Pedido, id)

    if not pedido_obtenido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    pedido_obtenido.cantidad = pedido_editar.cantidad
    pedido_obtenido.total = pedido_editar.total
    pedido_obtenido.usuario_id = pedido_editar.usuario_id
    pedido_obtenido.producto_id = pedido_editar.producto_id

    db.commit()
    db.refresh(pedido_obtenido)

    return pedido_obtenido

##########################
# METODO DELETE
##########################

@pedido_router.delete(
    '/{id}',
    responses=DICT_NOT_FOUND,
    response_model=list[PedidoPublic],
)
async def eliminar_pedido(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    pedido_obtenido = db.get(Pedido, id)

    if pedido_obtenido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    db.delete(pedido_obtenido)
    db.commit()

    return db.exec(select(Pedido)).all()

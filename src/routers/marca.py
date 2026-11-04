from typing import Annotated
from fastapi import HTTPException, Path, APIRouter, Depends
from database import get_db
from models.marca import Marca, MarcaBase, MarcaCreate, MarcaPublic
from models.anidados import MarcaNested
from sqlmodel import Session, select

from fastapi_pagination import Page, paginate




marca_router = APIRouter()

DICT_NOT_FOUND: dict = {
    404: {
        "description": "Si la marca no se encuentra en la lista",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Marca no encontrada"
                }
            }
        }
    }
}

##########################
# METODOS GET
##########################

@marca_router.get('/', response_model=Page[MarcaPublic])
async def get_marcas(db: Session = Depends(get_db)):
    marcas = db.exec(select(Marca)).all()
    return paginate (
        marcas
    )

@marca_router.get(
    '/{id}',
    responses=DICT_NOT_FOUND,
    response_model=MarcaNested
)
async def get_marca_id(id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")], db: Session = Depends(get_db)):
    marca_obtenida = db.get(Marca, id)
    if not marca_obtenida:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca_obtenida

##########################
# METODO POST 
##########################

@marca_router.post(
    '/',
    response_model=MarcaPublic,
    status_code=201
)
async def agregar_marca(nueva_marca: MarcaCreate, db: Session = Depends(get_db)):
    marca_db = Marca.model_validate(nueva_marca)

    db.add(marca_db)
    db.commit()
    db.refresh(marca_db)

    return marca_db

    
##########################
# METODO PUT
##########################

@marca_router.put(
    '/{id}',
    responses=DICT_NOT_FOUND,
    response_model=MarcaPublic
)
async def actualizar_marca(
    id: Annotated[int, Path(gt=0)],
    marca_editar: MarcaCreate,
    db: Session = Depends(get_db)
):

    marca_obtenida = db.get(Marca, id)

    if not marca_obtenida:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    marca_obtenida.nombre = marca_editar.nombre

    db.commit()
    db.refresh(marca_obtenida)

    return marca_obtenida

##########################
# METODO DELETE
##########################

@marca_router.delete(
    '/{id}',
    responses=DICT_NOT_FOUND,
    response_model=list[MarcaPublic],
)
async def eliminar_marca(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db)
):
    marca_obtenida = db.get(Marca, id)

    if marca_obtenida is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    db.delete(marca_obtenida)
    db.commit()

    return db.exec(select(Marca)).all()

from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.marca import Marca, MarcaPublic
    from models.pedido import Pedido
from src.models.marca import MarcaPublic

#MODELO BASE DE PRODUCTO
class ProductoBase(SQLModel):
    modelo: str= Field(max_length=90)
    talle: float
    precio:int
    activo:bool
    marca_id: int | None = Field(default = None, foreign_key="marca.id")

#MODELO TABLA DE PRODUCTO
class Producto(ProductoBase, table=True):
    id: int| None = Field(default=None, primary_key=True)
    marca: "Marca | None" = Relationship(back_populates="productos")
    pedidos: list["Pedido"] = Relationship(back_populates="producto")

#MODEL CREACION DE MARCA
class ProductoCreate(ProductoBase):
    pass

#MODELO DE LECTURA DE PRODUCTO
class ProductoPublic(ProductoBase):
    id:int

#MODELO NESTED
class ProductoPublicNested(ProductoPublic):
    marca: MarcaPublic | None=None
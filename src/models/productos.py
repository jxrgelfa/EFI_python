from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from models.marca import Marca


# MODELO BASE DE PRODUCTO
class ProductoBase(SQLModel):
    modelo: str = Field(max_length=90)
    talle: float
    precio: int
    activo: bool
    marca_id: int | None = Field(default=None, foreign_key="marca.id")


# MODELO TABLA DE PRODUCTO
class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: Optional[Marca] = Relationship(back_populates="productos")
    pedidos: list["Pedido"] = Relationship(back_populates="producto")


# MODELO CREACION DE PRODUCTO
class ProductoCreate(ProductoBase):
    pass


# MODELO DE LECTURA DE PRODUCTO
class ProductoPublic(ProductoBase):
    id: int

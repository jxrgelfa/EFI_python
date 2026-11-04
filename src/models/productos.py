from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from models.marca import Marca


# MODELO BASE DE PRODUCTO
class ProductoBase(SQLModel):
    nombre: str = Field(max_length=90)
    descripcion: str | None = None
    talle: float
    stock: int = Field(default=0, ge=0)
    imagen_url: str | None = None
    precio: int
    activo: bool = Field(default=True)
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

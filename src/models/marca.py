from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.productos import Producto, ProductoPublic
#MODELO BASE DE MARCA
class MarcaBase(SQLModel):
    nombre: str = Field(max_length=90)

#MODELO TABLA DE MARCA
class Marca(MarcaBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    #la marca tiene lista de productos
    productos: list["models.producto.Producto"] = Relationship(back_populates="marca")

#MODELO CREACION DE MARCA
class MarcaCreate(MarcaBase):
    pass

#MODELO DE LECTURA DR MARCA
class MarcaPublic(MarcaBase):
    id:int

#MODELO NESTED
class MarcaPublicNested(MarcaPublic):
    productos: list["models.producto.ProductoPublic"] = []
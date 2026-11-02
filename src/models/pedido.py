from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.productos import Producto, ProductoPublic


from models.usuario import Usuario, UsuarioPublic

#MODELO BASE DE PEDIDO
class PedidoBase(SQLModel):
    cantidad: int = Field(default=1)
    total: int
    usuario_id: int| None= Field(default=None, foreign_key="usuario.id")
    producto_id: int| None= Field(default=None, foreign_key="producto.id")

#MODELO TABLA DE PEDIDO
class Pedido(PedidoBase, table=True):
    id:int | None = Field(default=None, primary_key=True)
    usuario: Optional["Usuario"] = Relationship(back_populates="pedidos")
    producto: Optional["Producto"] = Relationship(back_populates="pedidos")

#MODELO CREACION DE PEDIDO
class PedidoCreate(PedidoBase):
    pass

#MODELO DE LECTURA DE PEDIDO
class PedidoPublic(PedidoBase):
    id:int

#MODELO NESTED
class PedidoPublicNested(PedidoPublic):
    usuario:  Optional["UsuarioPublic"] = None
    producto: Optional["ProductoPublic"] = None

from models.productos import ProductoPublic

PedidoPublicNested.model_rebuild()
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.pedido import Pedido, PedidoPublic
#EL MODELO BASE: Contiene los campos comunes a todos; sin crear una tabla
class UsuarioBase(SQLModel):
    nombre: str 
    email: str = Field(unique=True)
    activo: bool = Field(default=True)
   

#EL MODELO DE TABLA: Hereda de Base, agrega el ID y se guarda en la DB
class Usuario(UsuarioBase, table=True): #Table True indica que creará una tabla en la db
    id: int | None = Field(default=None, primary_key=True)
    contrasena: str
    #El usuario tiene lista de pedidos
    pedidos: list["Pedido"] = Relationship(back_populates="usuario")

#ESQUEMA DE AUTENTICACION
class UsuarioLogin(SQLModel):
    email: str
    contrasena: str

#EL MODELO DE CREACIÓN: Lo que el usuario envía (No tiene ID)
class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(min_length=6)

#EL MODELO DE LECTURA (Público): Lo que devolvemos al usuario
class UsuarioPublic(UsuarioBase):
    id: int 

#EL MODELO NESTED
class UsuarioPublicNested(UsuarioPublic):
    pedidos: list["PedidoPublic"] = []
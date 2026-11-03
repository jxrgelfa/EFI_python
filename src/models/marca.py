from sqlmodel import Field, Relationship, SQLModel


# MODELO BASE DE MARCA
class MarcaBase(SQLModel):
    nombre: str = Field(max_length=90)


# MODELO TABLA DE MARCA
class Marca(MarcaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # la marca tiene lista de productos
    productos: list["Producto"] = Relationship(back_populates="marca")


# MODELO CREACION DE MARCA
class MarcaCreate(MarcaBase):
    pass


# MODELO DE LECTURA DE MARCA
class MarcaPublic(MarcaBase):
    id: int

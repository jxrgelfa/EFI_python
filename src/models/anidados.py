from .marca import MarcaPublic
from .productos import ProductoPublic
from .usuario import UsuarioPublic
from .pedido import PedidoPublic


# --- PRODUCTO & MARCA ---
class ProductoNested(ProductoPublic):
    marca: MarcaPublic | None = None


class MarcaNested(MarcaPublic):
    productos: list[ProductoPublic] = []


# --- PEDIDO & USUARIO ---
class PedidoNested(PedidoPublic):
    usuario: UsuarioPublic | None = None
    producto: ProductoPublic | None = None


class UsuarioNested(UsuarioPublic):
    pedidos: list[PedidoPublic] = []

"""Modelos SQLModel para la base de datos."""
from src.models.marca import Marca, MarcaCreate, MarcaPublic, MarcaPublicNested
from src.models.pedido import Pedido, PedidoCreate, PedidoPublic, PedidoPublicNested
from src.models.productos import Producto, ProductoCreate, ProductoPublic, ProductoPublicNested
from src.models.usuario import Usuario, UsuarioCreate, UsuarioLogin, UsuarioPublic, UsuarioPublicNested

__all__ = [
    "Marca", "MarcaCreate", "MarcaPublic", "MarcaPublicNested",
    "Pedido", "PedidoCreate", "PedidoPublic", "PedidoPublicNested",
    "Producto", "ProductoCreate", "ProductoPublic", "ProductoPublicNested",
    "Usuario", "UsuarioCreate", "UsuarioLogin", "UsuarioPublic", "UsuarioPublicNested",
]

# Reconstruir esquemas anidados para que Pydantic y Swagger (/docs) resuelvan las referencias circulares
UsuarioPublicNested.model_rebuild(_types_namespace={"PedidoPublic": PedidoPublic})
PedidoPublicNested.model_rebuild(
    _types_namespace={"UsuarioPublic": UsuarioPublic, "ProductoPublicNested": ProductoPublicNested}
)
MarcaPublicNested.model_rebuild(
    _types_namespace={
        "ProductoPublic": ProductoPublic,
        "models": type("obj", (), {"producto": type("obj", (), {"ProductoPublic": ProductoPublic})}),
    }
)
ProductoPublicNested.model_rebuild(_types_namespace={"MarcaPublic": MarcaPublic})
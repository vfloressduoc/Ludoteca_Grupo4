from django.contrib import admin

#IMPORTAMOS AL USUARIO
from .models import Usuario
from .models import Categoria
from .models import Proveedor
from .models import Producto
from .models import CarritoProducto
from .models import Carrito


# Register your models here.
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(CarritoProducto)
admin.site.register(Carrito)













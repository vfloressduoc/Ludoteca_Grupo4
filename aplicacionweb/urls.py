from django.urls import path, include
from . import views
from django.contrib import admin
#Pantallas iniciales
from .views import home, cooperativo, deckbuilding, eurogames, familiar, solitarios

#Pantallas de usuario
from .views import iniciar_sesion
from .views import registrousuario #Verificar si esto aun tiene utilidad
from .views import recuperarcontrasena
from .views import editarperfil

#Pant para panel de moderacion
from .views import panel_moderacion
from .views import form_mod_usuario
from .views import form_usuario
from .views import form_del_usuario

#registro de clientes
from .views import reg_clientes
from .views import iniciar_sesion
from .views import cerrar_sesion

#Panel de administracion para manejar productos
from .views import panel_create_productos
from .views import panel_productos
from .views import form_mod_producto
from .views import form_del_producto

from .views import agregar_al_carrito
from .views import carrito_compras
from .views import quitar_del_carrito
from .views import ordenes_compra
from .views import ver_pedidos
from .views import realizar_compra
from .views import ver_todos_pedidos
from .views import panel_pedidos
from .views import borrar_pedido
from .views import recuperar_contrasena
from .views import cambiar_contrasena




urlpatterns = [
    path('', home, name='home'),
    path('cooperativo/', cooperativo, name='cooperativo'),
    path('deckbuilding/', deckbuilding, name='deckbuilding'),
    path('eurogames/', eurogames, name='eurogames'),
    path('familiar/', familiar, name='familiar'),
    path('solitarios/', solitarios, name='solitarios'),
    path('iniciarsesion/', iniciar_sesion, name='iniciarsesion'),
    path('registrousuario/', registrousuario, name='registrousuario'),
    path('recuperarcontrasena/', recuperarcontrasena, name='recuperarcontrasena'),
    path('editarperfil/', editarperfil, name='editarperfil'),
    path('panel_moderacion/', panel_moderacion, name='panel_moderacion'),
    
    path('form_usuario/', form_usuario, name='form_usuario'),
    path('form_mod_usuario/<id>', form_mod_usuario, name='form_mod_usuario'),
    path('form_del_usuario/<id>', form_del_usuario, name='form_del_usuario'),
    path('reg_clientes/', reg_clientes, name='reg_clientes'),
    path('iniciar_sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('panel_create_productos/', panel_create_productos, name='panel_create_productos'),
    path('panel_productos/', panel_productos, name='panel_productos'),
    path('form_mod_producto/<int:id>/', views.form_mod_producto, name='form_mod_producto'),
    path('form_del_producto/<id>', form_del_producto, name='form_del_producto'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito_compras/', carrito_compras, name='carrito_compras'),
    path('quitar_del_carrito/<int:producto_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('ordenes_compra/', views.ordenes_compra, name='ordenes_compra'),
    path('realizar_compra/', views.realizar_compra, name='realizar_compra'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('ver_todos_pedidos/', views.ver_todos_pedidos, name='ver_todos_pedidos'),
    path('panel_pedidos/', views.panel_pedidos, name='panel_pedidos'),
    path('borrar_pedido/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),
    path('recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('cambiar_contrasena/<int:user_id>/', cambiar_contrasena, name='cambiar_contrasena'),
]
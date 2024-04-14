from django.urls import path

from .views import home
from .views import cooperativo
from .views import deckbuilding
from .views import eurogames
from .views import familiar
from .views import solitarios
from .views import iniciarsesion
from .views import registrousuario
from .views import recuperarcontrasena
from .views import editarperfil
#Mimportaciones para panel de moderacion
from .views import panel_moderacion
from .views import form_mod_usuario
#form_usuario
from .views import form_usuario
#form delete usuario
from .views import form_del_usuario
#registro de clientes
from .views import reg_clientes

urlpatterns = [
    path('', home, name='home'),
    path('cooperativo/', cooperativo, name='cooperativo'),
    path('deckbuilding/', deckbuilding, name='deckbuilding'),
    path('eurogames/', eurogames, name='eurogames'),
    path('familiar/', familiar, name='familiar'),
    path('solitarios/', solitarios, name='solitarios'),
    path('iniciarsesion/', iniciarsesion, name='iniciarsesion'),
    path('registrousuario/', registrousuario, name='registrousuario'),
    path('recuperarcontrasena/', recuperarcontrasena, name='recuperarcontrasena'),
    path('editarperfil/', editarperfil, name='editarperfil'),
    path('panel_moderacion/', panel_moderacion, name='panel_moderacion'),
    
    #form_usuario
    path('form_usuario/', form_usuario, name='form_usuario'),
    #form_mod_usuario
    path('form_mod_usuario/<id>', form_mod_usuario, name='form_mod_usuario'),
    #form_del_usuario
    path('form_del_usuario/<id>', form_del_usuario, name='form_del_usuario'),
    #registro de clientes
    path('reg_clientes/', reg_clientes, name='reg_clientes'),
    
]


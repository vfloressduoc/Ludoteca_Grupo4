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
]


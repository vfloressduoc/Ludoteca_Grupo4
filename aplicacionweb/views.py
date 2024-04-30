from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm  #formulario de usuario
from .forms import ClienteForm  #formulario de usuario
#para iniciar sesion
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .forms import ProductoForm
from .models import Producto, Carrito, CarritoProducto
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Pedido
from .models import PedidoProducto
from .models import UserProfile

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponseRedirect
from .models import Categoria, Proveedor



# Create your views here.

#VISTAS GENERALES
def home(request):
    return render(request, 'aplicacionweb/home.html')

def cooperativo(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/cooperativo.html', {'productos': productos})

def deckbuilding(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/deckbuilding.html', {'productos': productos})

def eurogames(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/eurogames.html', {'productos': productos})

def familiar(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/familiar.html', {'productos': productos})

def solitarios(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/solitarios.html', {'productos': productos})

def iniciarsesion(request):
    return render(request, 'aplicacionweb/iniciar_sesion.html')

def registrousuario(request):
    return render(request, 'aplicacionweb/registrousuario.html')

def recuperarcontrasena(request):
    return render(request, 'aplicacionweb/recuperarcontrasena.html')

#*DEFINICION DE CLASES (COMO SE VERÁ LA PAGINA)

#USUARIO
#EDITAR DATOS DE UN USUARIO EXISTENTE (Usando 'User' de Django)
class EditarPerfilForm(UserChangeForm):
    password = None  # No incluir el campo de contraseña en el formulario
    class Meta:
        model = User
        fields = ('username', 'email', )

@login_required
def editarperfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'aplicacionweb/editarperfil.html', {'form': form, 'mensaje': 'Perfil actualizado correctamente'})
    else:
        form = EditarPerfilForm(instance=request.user)
        return render(request, 'aplicacionweb/editarperfil.html', {'form': form})

#VER USUARIOS
def panel_moderacion(request):
    usuarios = User.objects.all() # esto es un SELECT * FROM auth_user
    
    context = {
        'usuarios': usuarios
    }
    
    return render(request, 'aplicacionweb/panel_moderacion.html', context)


#CREAR USUARIO (Usando 'User' de Django)
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    is_superuser = forms.BooleanField(required=False)
    avatar = forms.ImageField(required=False)  # Nuevo campo
    palabra_clave = forms.CharField(max_length=100, required=False)  # Nuevo campo

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', 'avatar', 'palabra_clave') 


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    palabra_clave = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'palabra_clave')

def form_usuario(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            user_form = CustomUserCreationForm()
            profile_form = UserProfileForm()

            datos = {'user_form': user_form, 'profile_form': profile_form, 'mensaje': "Usuario guardado exitosamente"}
        else:
            datos = {'user_form': user_form, 'profile_form': profile_form}
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
        datos = {'user_form': user_form, 'profile_form': profile_form}

    return render(request, 'aplicacionweb/form_usuario.html', datos)
            

#MODIFICAR UN USUARIO (Usando 'User' de Django)
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_superuser', )

def form_mod_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    profile, created = UserProfile.objects.get_or_create(user=usuario)
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=usuario)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'aplicacionweb/form_mod_usuario.html', {'user_form': user_form, 'profile_form': profile_form, 'mensaje': 'Usuario modificado correctamente'})
    else:
        user_form = CustomUserChangeForm(instance=usuario)
        profile_form = UserProfileForm(instance=profile)
        return render(request, 'aplicacionweb/form_mod_usuario.html', {'user_form': user_form, 'profile_form': profile_form})
    

#ELIMINAR UN USUARIO (Usando 'User' de Django)
def form_del_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    
    return redirect(to="panel_moderacion")



#REGISTRO COMO CLIENTE (Usando 'User' de Django)
from django.contrib.auth import authenticate, login

def reg_clientes(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            UserProfile.objects.create(user=user, avatar=profile_form.cleaned_data['avatar'], palabra_clave=profile_form.cleaned_data['palabra_clave'])
            
            # Autenticar al usuario y luego iniciar sesión
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, new_user)

            return redirect('home')
        else:
            context = {'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'aplicacionweb/reg_clientes.html', context)
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'aplicacionweb/reg_clientes.html', context)

#INICIO DE SESION
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['contrasena']
        if User.objects.filter(username=username).exists():  # Verificar si el usuario existe
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta')
                return redirect('iniciar_sesion')  # Cambiado aquí
        else:
            messages.error(request, 'El usuario no existe')
            return redirect('iniciar_sesion')  # Cambiado aquí
    else:
        return render(request, 'aplicacionweb/iniciar_sesion.html')

#CERRAR SESION
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

#REGISTRO DE USUARIOS (Usando 'User' de Django)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# ***** MANIPULAR PRODUCTOS CRUD *****


#VER LOS PRODUCTOS
def panel_productos(request):
    productos = Producto.objects.all() #Esto es un SELECT * FROM desde la tabla de productos
    
    context = {
        'productos': productos
    }
    
    return render(request, 'aplicacionweb/panel_productos.html', context)

#** CREAR PRODUCTOS
def panel_create_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ProductoForm()  # Crea una nueva instancia del formulario
            datos = {'form': form, 'mensaje': "Producto guardado exitosamente"}
        else:
            datos = {'form': form}
    else:
        form = ProductoForm()
        datos = {'form': form}
    
    return render(request, 'aplicacionweb/panel_create_productos.html', datos)

#MODIFICAR PRODUCTOS
def form_mod_producto(request, id):
    producto = Producto.objects.get(idProducto=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('panel_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'aplicacionweb/form_mod_producto.html', {'form': form})

#ELIMINAR PRODUCTOS
def form_del_producto(request, id):
    producto = Producto.objects.get(idProducto=id)
    producto.delete()
    
    return redirect(to="panel_productos")


#CARRITO DE COMPRAS

#DEF PARA AGREGAR ITEM A CARRITO (Se usa tanto para el boton comprar como para aumentar la cantidad de un item en el carrito)
@login_required
def agregar_al_carrito(request, nombre_producto):
    producto = get_object_or_404(Producto, nombreProducto=nombre_producto)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    carrito_producto, creado = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        carrito_producto.cantidad += 1
        carrito_producto.save()
    return redirect('carrito_compras')

#PAGINA PARA VER EL CARRITO
@login_required
def carrito_compras(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_productos = CarritoProducto.objects.filter(carrito=carrito)
    total = sum(item.producto.precioProducto * item.cantidad for item in carrito_productos)
    return render(request, 'aplicacionweb/carrito_compras.html', {'carrito_productos': carrito_productos, 'total': total})

#QUITAR ITEM DEL CARRITO
@login_required
def quitar_del_carrito(request, nombre_producto):
    producto = get_object_or_404(Producto, nombreProducto=nombre_producto)
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito_producto = get_object_or_404(CarritoProducto, carrito=carrito, producto=producto)
    if carrito_producto.cantidad > 1:
        carrito_producto.cantidad -= 1
        carrito_producto.save()
    else:
        carrito_producto.delete()
    return redirect('carrito_compras')

@login_required
def ordenes_compra(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'aplicacionweb/ordenes_compra.html', {'pedidos': pedidos})

#REALIZAR COMPRA
@login_required
def realizar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    pedido = Pedido.objects.create(usuario=request.user)
    for carrito_producto in carrito.carritoproducto_set.all():
        PedidoProducto.objects.create(
            pedido=pedido,
            producto=carrito_producto.producto,
            cantidad=carrito_producto.cantidad
        )
    carrito.carritoproducto_set.all().delete()
    return redirect('ordenes_compra')

#VER PEDIDOS REALIZADOS
def ver_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

#PANEL PEDIDOS PARA ADMINISTRADORES
def panel_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'aplicacionweb/panel_pedidos.html', {'pedidos': pedidos})

#VER TODOS LOS PEDIDOS EN LA TABLA DE PEDIDOS (NO SOLO DEL USUARIO LOGEADO)
def ver_todos_pedidos(request):
    if request.user.is_superuser:  # Asegurarse de que solo los superusuarios pueden ver todos los pedidos
        pedidos = Pedido.objects.all()
        return render(request, 'panel_pedidos.html', {'pedidos': pedidos})
    else:
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para ver esta página.'})

#BORRAR PEDIDO
def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.user.is_superuser:  # Solo los superusuarios pueden borrar pedidos
        pedido.delete()
    return redirect('panel_pedidos')

#RECUPERAR CONTRASEÑA
def recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST['email']
        palabra_clave = request.POST['palabra_clave']

        try:
            user = User.objects.get(email=email)
            user_profile = UserProfile.objects.get(user=user, palabra_clave=palabra_clave)
            return redirect('cambiar_contrasena', user_id=user.id)
        except ObjectDoesNotExist:
            return render(request, 'aplicacionweb/recuperar_contrasena.html', {'error': 'No existe un usuario con ese correo electrónico y palabra clave.'})

    return render(request, 'aplicacionweb/recuperar_contrasena.html')
    
#CAMBIOA ACEPTADO   
class SetPasswordFormWithoutOldPassword(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super(SetPasswordFormWithoutOldPassword, self).__init__(user, *args, **kwargs)
        if 'old_password' in self.fields:
            del self.fields['old_password']

    def clean_old_password(self):
        #? No hacer nada en este método?
        pass

from django.contrib.auth.decorators import login_required

def cambiar_contrasena(request, user_id):
    if request.user.is_authenticated:
        # Si el usuario está conectado, redirigir a la página de inicio
        return redirect('home')

    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = SetPasswordFormWithoutOldPassword(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante, para que el usuario no sea desconectado
            return redirect('home')
    else:
        form = SetPasswordFormWithoutOldPassword(user)
    return render(request, 'aplicacionweb/cambiar_contrasena.html', {'form': form})


# ** AGREGAR DATOS INICIALES A LA BBDD: Esto cargo las 5 categorias, 2 proveedores y los productos que se ven en las pantallas **
def agregar_categorias(request):
    if request.method == 'POST':
        categoria_familiar, _ = Categoria.objects.get_or_create(nombre='Familiar')
        categoria_cooperativo, _ = Categoria.objects.get_or_create(nombre='Cooperativo')
        categoria_eurogame, _ = Categoria.objects.get_or_create(nombre='Eurogame')
        categoria_deckbuilding, _ = Categoria.objects.get_or_create(nombre='Deckbuilding')
        categoria_solitarios, _ = Categoria.objects.get_or_create(nombre='Solitarios')

        proveedor_nacional, _ = Proveedor.objects.get_or_create(tipo='Nacional')
        proveedor_extranjero, _ = Proveedor.objects.get_or_create(tipo='Extranjero')

        descripcion_dixit = 'Libellud | Dixit Classic | Juego de Mesa de Imaginación y Creatividad Ganador de Varios Premios| A Partir de 8 Años | De 3 a 8 Jugadores | 30 Minutos por Partida | En Español'
        Producto.objects.get_or_create(nombreProducto='Dixit', precioProducto=25000, descripcionProducto=descripcion_dixit, imagenProducto='productos/dixit.png', categoria=categoria_familiar, proveedor=proveedor_nacional)

        descripcion_arkham = 'Secretos de la Orden | Juego de Mesa | -6 Jugadores | A Partir de 14 años | 2-3 Horas de Tiempo de Juego'
        Producto.objects.get_or_create(nombreProducto='Arkham Horror 3* Edición', precioProducto=35000, descripcionProducto=descripcion_arkham, imagenProducto='productos/arkham.png', categoria=categoria_cooperativo, proveedor=proveedor_extranjero)

        descripcion_7wonders = 'Juego de Cartas en Español Recomendado a Partir de 10 Años de Edad Juego de 3 a 7 Jugadores Con una duración de 30 Minutos por partida Apto para personas con daltonismo.'
        Producto.objects.get_or_create(nombreProducto='7 Wonders Nueva Edición', precioProducto=45000, descripcionProducto=descripcion_7wonders, imagenProducto='productos/7wonders.png', categoria=categoria_familiar, proveedor=proveedor_nacional)

        descripcion_pandemic = 'Z-Man Games | Pandemic | Juego de Mesa Cooperativo para Adultos y Familias | A Partir de 8 Años | De 2 a 4 Jugadores | 45 Minutos por Partida | Español'
        Producto.objects.get_or_create(nombreProducto='Pandemic', precioProducto=20000, descripcionProducto=descripcion_pandemic, imagenProducto='productos/pandemic.png', categoria=categoria_cooperativo, proveedor=proveedor_nacional)

        descripcion_brass = 'Roxley Games- Brass Latón: Birmingham, colores variados (ROX402) , color/modelo surtido'
        Producto.objects.get_or_create(nombreProducto='Brass Birmingham', precioProducto=100000, descripcionProducto=descripcion_brass, imagenProducto='productos/brass.png', categoria=categoria_eurogame, proveedor=proveedor_extranjero)

        descripcion_dune = 'Asmodee - Dune: Imperium, Juego de Mesa, 1-4 Jugadores, 13+ Años, Edición en Italiano'
        Producto.objects.get_or_create(nombreProducto='Dune Imperium', precioProducto=45000, descripcionProducto=descripcion_dune, imagenProducto='productos/dune.png', categoria=categoria_eurogame, proveedor=proveedor_extranjero)

        descripcion_marvel = 'El juego de Cartas | Juego de Estrategia y Superhéroes Cooperativo | A Partir de 14 Años | De 1 a 4 Jugadores | 45-90 Minutos por Partida | Español'
        Producto.objects.get_or_create(nombreProducto='Marvel Champions', precioProducto=55000, descripcionProducto=descripcion_marvel, imagenProducto='productos/marvelchampions.png', categoria=categoria_deckbuilding, proveedor=proveedor_extranjero)

        descripcion_hero = 'Devir - Hero Realms, Juego de Cartas 12 años, Fácil y Divertido (BGHR)'
        Producto.objects.get_or_create(nombreProducto='Hero Realms', precioProducto=18000, descripcionProducto=descripcion_hero, imagenProducto='productos/herorealms.png', categoria=categoria_deckbuilding, proveedor=proveedor_extranjero)

        descripcion_7continent = 'Core Box 2nd Edition - Juego básico de iniciación (versión inglesa)'
        Producto.objects.get_or_create(nombreProducto='The 7th Continent (Inglés)', precioProducto=80000, descripcionProducto=descripcion_7continent, imagenProducto='productos/7thcontinent.png', categoria=categoria_solitarios, proveedor=proveedor_extranjero)
        
        descripcion_viernes = 'Edge Studio | Viernes | Juego de Cartas de Estrategia para un Solo Jugador | A Partir de 10 Años | Juego en solitario | 30 Minutos por Partida |'
        Producto.objects.get_or_create(nombreProducto='Viernes', precioProducto=20000, descripcionProducto=descripcion_viernes, imagenProducto='productos/viernes.png', categoria=categoria_solitarios, proveedor=proveedor_nacional)
        return redirect('home')

    return render(request, 'home.html')



#** VER CATEGORIAS
def categorias_proveedores(request):
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()  
    return render(request, 'aplicacionweb/categorias_proveedores.html', {'categorias': categorias, 'proveedores': proveedores})

# BORRAR CATEGORIA

def borrar_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)  
    proveedor.delete()
    return redirect('categorias_proveedores')


def borrar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('categorias_proveedores')

#vista para traer playlist al home.

def playlist_view(request):
    return render(request, 'home.html')

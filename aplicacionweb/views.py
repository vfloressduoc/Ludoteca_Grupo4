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
from django.contrib.auth.decorators import login_required




# Create your views here.

#VISTAS GENERALES
def home(request):
    return render(request, 'aplicacionweb/home.html')

def cooperativo(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/cooperativo.html', {'productos': productos})

#! El footer (parte inferior redes sociales) de la pagina se sobrepone al boton comprar del segundo producto, tuve que desactivarlo por ahora 
def deckbuilding(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/deckbuilding.html', {'productos': productos})

#! El footer (parte inferior redes sociales) de la pagina se sobrepone al boton comprar del segundo producto, tuve que desactivarlo por ahora 
def eurogames(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/eurogames.html', {'productos': productos})

#! El footer (parte inferior redes sociales) de la pagina se sobrepone al boton comprar del segundo producto, tuve que desactivarlo por ahora 
def familiar(request):
    productos = Producto.objects.all()
    return render(request, 'aplicacionweb/familiar.html', {'productos': productos})

#! El footer (parte inferior redes sociales) de la pagina se sobrepone al boton comprar del segundo producto, tuve que desactivarlo por ahora 
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
#TODO Organizar las clases de acuerdo a la estructura de la pagina web, quitar las que no esten en uso.
#TODO Cambiar el nombre de las clases a algo mas descriptivo, ej: 'form_usuario' a 'form_create_usuario'.
#TODO las html que tienen los productos para ver deberian recurrir a la info de nuestras tablas para mostrarlos y que sea dinamico, no a una imagen o info pegada en el html.

#USUARIO
#EDITAR DATOS DE UN USUARIO EXISTENTE (Usando 'User' de Django)
class EditarPerfilForm(UserChangeForm):
    password = None  # No incluir el campo de contraseña en el formulario
    class Meta:
        model = User
        fields = ('username', 'email', )

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

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', )

def form_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            form = CustomUserCreationForm()  # Crea una nueva instancia del formulario
            datos = {'form': form, 'mensaje': "Usuario guardado exitosamente"}
        else:
            datos = {'form': form}
    else:
        form = CustomUserCreationForm()
        datos = {'form': form}
            
    return render(request, 'aplicacionweb/form_usuario.html', datos)
            

#MODIFICAR UN USUARIO (Usando 'User' de Django)
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_superuser', )

def form_mod_usuario(request, id):
    usuario = User.objects.get(id=id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return render(request, 'aplicacionweb/form_mod_usuario.html', {'form': form, 'mensaje': 'Usuario modificado correctamente'})
    else:
        form = CustomUserChangeForm(instance=usuario)
        return render(request, 'aplicacionweb/form_mod_usuario.html', {'form': form})
    

#ELIMINAR UN USUARIO (Usando 'User' de Django)
def form_del_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    
    return redirect(to="panel_moderacion")



#REGISTRO COMO CLIENTE (Usando 'User' de Django)
def reg_clientes(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'aplicacionweb/reg_clientes.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'aplicacionweb/reg_clientes.html', {'form': form})

#INICIO DE SESION
#! Feedback: Al ingresar un usuario incorrecto y posteriormente una contraseña incorrecta, persiste el mensaje "usuario incorrecto" y viseversa, se debe limpiar
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

# RECUPERACION DE CONTRASEÑA
#TODO Pendiente de implementar la 'recuperacion de contraseña'

# ***** MANIPULAR PRODUCTOS CRUD *****


#VER LOS PRODUCTOS
def panel_productos(request):
    productos = Producto.objects.all() #Esto es un SELECT * FROM desde la tabla de productos
    
    context = {
        'productos': productos
    }
    
    return render(request, 'aplicacionweb/panel_productos.html', context)

#CREAR PRODUCTOS
#TODO Feedback: Solicita un proveedor y una categoria que no aparecen, debemos cambiarlo en models. el tipo de datos a Char para ingresar dato (pendiente a que podria romper algo mas) o intentar que automaticamente inyecte esas categorias.
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

#BOTON PARA AGREGAR ITEM A CARRITO
#!Si no estas logeado se cae la web, debe solo enviar un mensaje para que se logee "Solo usuarios registrados"
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, idProducto=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    carrito_producto, creado = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        carrito_producto.cantidad += 1
        carrito_producto.save()
    return redirect('carrito_compras')

#PAGINA PARA VER EL CARRITO
@login_required
def carrito_compras(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito_productos = CarritoProducto.objects.filter(carrito=carrito)
    return render(request, 'aplicacionweb/carrito_compras.html', {'carrito_productos': carrito_productos})

@login_required
def quitar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, idProducto=producto_id)
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito_producto = get_object_or_404(CarritoProducto, carrito=carrito, producto=producto)
    if carrito_producto.cantidad > 1:
        carrito_producto.cantidad -= 1
        carrito_producto.save()
    else:
        carrito_producto.delete()
    return redirect('carrito_compras')

#TODO Pendiente de implementar la logica del 'carrito de compra'
#TODO Pendiente de implementar 'orden de compra' luego de comprar un carrito


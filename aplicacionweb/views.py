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




# Create your views here.

#VISTAS GENERALES
def home(request):
    return render(request, 'aplicacionweb/home.html')

def cooperativo(request):
    return render(request, 'aplicacionweb/cooperativo.html')

def deckbuilding(request):
    return render(request, 'aplicacionweb/deckbuilding.html')

def eurogames(request):
    return render(request, 'aplicacionweb/eurogames.html')

def familiar(request):
    return render(request, 'aplicacionweb/familiar.html')

def solitarios(request):
    return render(request, 'aplicacionweb/solitarios.html')

def iniciarsesion(request):
    return render(request, 'aplicacionweb/iniciar_sesion.html')

def registrousuario(request):
    return render(request, 'aplicacionweb/registrousuario.html')

def recuperarcontrasena(request):
    return render(request, 'aplicacionweb/recuperarcontrasena.html')

#USUARIO
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
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['contrasena']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales de usuario incorrecto')
            return redirect('iniciar')
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

#CREAR PRODUCTOS
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

# ***** AGREGAR PRODUCTOS AL CARRITO *****




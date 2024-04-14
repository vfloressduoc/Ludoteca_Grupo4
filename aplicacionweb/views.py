from django.shortcuts import render, redirect, get_object_or_404 #redirect, get_object_or_404 para el cart
from .models import Usuario
from .forms import UsuarioForm  #formulario de usuario
from django.contrib.auth.decorators import login_required #para el cart
from django.contrib import messages #para el cart
from .models import Cart #para el cart


# Create your views here.
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
    return render(request, 'aplicacionweb/iniciarsesion.html')

def registrousuario(request):
    return render(request, 'aplicacionweb/registrousuario.html')

def recuperarcontrasena(request):
    return render(request, 'aplicacionweb/recuperarcontrasena.html')

def editarperfil(request):
    return render(request, 'aplicacionweb/editarperfil.html')

def form_del_usuario(request):
    return render(request, 'aplicacionweb/form_del_usuario.html')

#Metodo para listar y ver usuarios
def panel_moderacion(request):
    usuarios = Usuario.objects.all() # SELECT * FROM Usuario
    
    context = {
        'usuarios': usuarios
        }
    
    datos = {'usuarios': usuarios}
    return render(request, 'aplicacionweb/panel_moderacion.html', context)

#form_usuario
# def form_usuario(request):
#     form = UsuarioForm()  # Crea una nueva instancia de tu formulario
#     return render(request, 'aplicacionweb/form_usuario.html', {'form': form}) #El form no esta en la guia lo tuve que agregar para que se vieran los items


#vista de formulario de usuario para crear un nuevo usuario
def form_usuario(request):
    #el view sera el encargado de entregar el formulario al template
    if request.method == 'POST':
        #con un request rescatamos los datos del formulario
        form = UsuarioForm(request.POST)
        
        #verificamos si el formulario es valido
        if form.is_valid():
            #guardamos el formulario
            form.save()
            datos = {'form': form, 'mensaje': "Usuario guardado exitosamente"}
        else:
            datos = {'form': form}
    else:
        form = UsuarioForm()  # Crea una nueva instancia de tu formulario
        datos = {'form': form}
            
    return render(request, 'aplicacionweb/form_usuario.html', datos)
            

#vista de formulario de usuario para modificar un usuario
def form_mod_usuario(request, id):
#el id es el que se recibe por parametro apra que sepa a quien editar, es el campo del usuario que le vamos a dar, por ejemplo en este caso el correo electronico unico
#buscando los datos en la base de datos
#b buscamos el usuario por el correo
    usuario = Usuario.objects.get(email=id)
    datos = {
         'form' : UsuarioForm(instance=usuario)
     }   
    
    #ahora le entregamos los datos del usuario al formulario
    if request.method=='POST':
        
     #con request recuperamos los datos del formulario y le agregamos el id modificar
     form = UsuarioForm(data=request.POST, instance=usuario)  
     
     #validamos el formulario
     if form.is_valid():
            form.save()
            
            datos['mensaje'] = "Usuario modificado correctamente"
         
    return render(request, 'aplicacionweb/form_mod_usuario.html', datos)

#vista de formulario de usuario para eliminar un usuario
def form_del_usuario(request, id):
    usuario = Usuario.objects.get(email=id)
    usuario.delete()
    
    return redirect(to="panel_moderacion")


'''
CARRITO DE COMPRAS
'''
# @login_required
def carritodecompras(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.all()
    precio_total = sum(item.cantidad * item.precio for item in cart_items)

    context = {
        "cart_items": cart_items,
        "precio_total": precio_total,
    }

    return render(request, "aplicacionweb/carritodecompras.html", context)


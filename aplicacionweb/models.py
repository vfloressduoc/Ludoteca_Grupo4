from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#NOTA: Para las imagenes tuve que instalar "python -m pip install Pillow" para que funcionara

# #CLASE DE USUARIO (esta tabla se puede quitar si se desea, ya que se esta usando la tabla User de Django)
class Usuario(models.Model):
    email = models.EmailField(max_length=200, verbose_name='Email', unique=True, primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido')
    nombreUsuario = models.CharField(max_length=50, unique=True, verbose_name='Usuario')
    contrasena = models.CharField(max_length=50, verbose_name='Contrasena')
    direccion = models.CharField(max_length=200, verbose_name='Direccion')
    
    def __str__(self):
        return self.get_code_name()
    
    def get_code_name(self):
        return f"Email asociado: {self.email} - {self.nombre} - {self.apellido}"
    
    
    
#CREANDO LAS CLASES
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    TIPOS_PROVEEDOR = [
        ('Nacional', 'Nacional'),
        ('Extranjero', 'Extranjero'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS_PROVEEDOR, default='Nacional')

    def __str__(self):
        return self.tipo

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=50, verbose_name='Nombre')
    precioProducto = models.IntegerField(verbose_name='Precio')
    descripcionProducto = models.TextField(max_length=200, verbose_name='Descripcion')
    imagenProducto = models.ImageField(upload_to='productos', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreProducto

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombreProducto}'

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username}'





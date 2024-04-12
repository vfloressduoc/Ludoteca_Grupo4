from django.db import models

# Create your models here.

#NOTA: Para las imagenes tuve que instalar "python -m pip install Pillow" para que funcionara

# #CLASE PARA REGISTRAR USUARIOS
class Usuario(models.Model):
    email = models.EmailField(max_length=200, verbose_name='Email', unique=True, primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido')
    nombreUsuario = models.CharField(max_length=50, verbose_name='Usuario')
    contrasena = models.CharField(max_length=50, verbose_name='Contraseña')
    direccion = models.CharField(max_length=200, verbose_name='Direccion')
    
    def __str__(self):
        return self.get_code_name()
    
    def get_code_name(self):
        return f"Email asociado: {self.email} - {self.nombre} - {self.apellido}"















# #CLASE PARA REGISTRAR CATEGORIAS: DIFERENCIA USUARIO DE ADMIN
# class tipoUsuario(models.Model):
#     idTipo = models.AutoField(primary_key=True)
#     nombreTipo = models.CharField(max_length=50, verbose_name='Nombre')
    
#     def __str__(self):
#         return self.nombreTipo
    
# #CLASE PARA REGISTRAR ADMINISTRADORES
# class Administrador(models.Model):
#     emailAdministrador = models.CharField(max_length=200, primary_key=True, verbose_name='Email')
#     nombreAdministrador = models.CharField(max_length=50, verbose_name='Nombre')
#     contraseñaAdministrador = models.CharField(max_length=50, verbose_name='Contraseña')
#     avatarAdministrador = models.ImageField(upload_to='administradores', null=True, blank=True)
#     tipoUsuario = models.ForeignKey('tipoUsuario', on_delete=models.CASCADE, related_name='administradores')
    
#     def __str__(self):
#         return self.nombreAdministrador


# #CLASE PARA REGISTRAR DIRECCIONES DE USUARIOS 
# class Direccion(models.Model):
#     idDireccion = models.AutoField(primary_key=True)
#     direccion = models.CharField(max_length=200, verbose_name='Direccion')
#     ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
#     codigoPostal = models.CharField(max_length=10, verbose_name='Codigo Postal')
#     usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='direcciones')
    
#     def __str__(self):
#         return self.direccion

#CLASE PARA REGISTRAR CATEGORIAS DE PRODUCTOS
# class Categoria(models.Model):
#     idCategoria = models.AutoField(primary_key=True)
#     nombreCategoria = models.CharField(max_length=50, verbose_name='Nombre')
    
#     def __str__(self):
#         return self.nombreCategoria

# #CLASE PARA REGISTRAR PRODUCTOS
# class producto(models.Model):
#     idProducto = models.AutoField(primary_key=True)
#     nombreProducto = models.CharField(max_length=50, verbose_name='Nombre')
#     precioProducto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
#     descripcionProducto = models.TextField(max_length=200, verbose_name='Descripcion')
#     imagenProducto = models.ImageField(upload_to='productos', null=True, blank=True)
#     categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productos')
    
#     def __str__(self):
#         return self.nombreProducto

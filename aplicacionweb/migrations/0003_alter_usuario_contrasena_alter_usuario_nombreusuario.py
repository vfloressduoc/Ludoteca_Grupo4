# Generated by Django 5.0.4 on 2024-04-14 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacionweb', '0002_remove_producto_categoria_remove_direccion_usuario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='contrasena',
            field=models.CharField(max_length=50, verbose_name='Contrasena'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombreUsuario',
            field=models.CharField(max_length=50, verbose_name='Usuario'),
        ),
    ]

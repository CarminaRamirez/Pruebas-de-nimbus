import os
from django.db import models

# Create your models here.


class Popups(models.Model):
    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='popups')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    def __str__(self):
        return self.titulo

    def extension(self):
        name, extension = os.path.splitext(self.imagen.name)
        return extension
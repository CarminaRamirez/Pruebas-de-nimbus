import os

from django.db import models
from star_ratings.models import Foo

# Create your models here.


class Novedad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    contenido = models.CharField(max_length=10000)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='novedades')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    youtube_url = models.CharField(null=True, blank=True, max_length=255)
    youtube_video_id = models.CharField(null=True, blank=True, max_length=255)
    estrellas = models.ForeignKey(Foo, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.titulo

    def extension(self):
        name, extension = os.path.splitext(self.imagen.name)
        return extension

#    def save(self, *args, **kwargs):
#        aux = self.youtube
#        if aux.find('/') > 0:
#            aux = self.youtube.split('/')
#            aux = aux[-1:]
#            self.youtube = aux[0]
#        super(Novedad, self).save(*args, **kwargs)

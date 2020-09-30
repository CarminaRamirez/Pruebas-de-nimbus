import os
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

# Create your models here.


class Banner(models.Model):
    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='banners')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()


    #ordenar por calificacion
    #Banner.objects.filter(ratings__isnull=False).order_by('ratings__average')


    def __str__(self):
        return self.titulo

    def extension(self):
        name, extension = os.path.splitext(self.imagen.name)
        return extension


class BannerReview(models.Model):
    RATING_RANGE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='rates')
    rating = models.IntegerField(choices=RATING_RANGE,)
    content = models.CharField(max_length=500)
    ratings = GenericRelation(Rating, related_query_name='banners')

    def __str__(self):
        return self.content
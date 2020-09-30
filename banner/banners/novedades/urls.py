from django.urls import path

from .views import (
                    eliminar_novedad,
                    agregar_editar,
                    listar,
                    detalle,
                    )
app_name = 'novedades'
urlpatterns = [
    path('', listar, name="listar_novedades"),
    path('<int:pk>/', agregar_editar, name='novedad_editar'),
    path('agregar/', agregar_editar, name='novedad_agregar'),
    path('<int:pk>/ver/', detalle, name='novedad_detalle'),
    path('delete/', eliminar_novedad, name='eliminar'),
]
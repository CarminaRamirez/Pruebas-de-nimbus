from django.urls import path, include

from .views import (home,
                    eliminar_banner,
                    agregar_editar,
                    listar,
                    )

app_name = 'banner'
urlpatterns = [
    # path('home', home, name='home'),
    path('', listar, name="listar_banners"),
    path('agregar/', agregar_editar, name='banner'),
    path('<int:pk>/', agregar_editar, name='banner_detalle'),
    path('delete/', eliminar_banner, name='eliminar'),

]
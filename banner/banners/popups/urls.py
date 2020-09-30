from django.urls import path

from .views import (
                    popup,
                    eliminar_popup,
                    agregar_editar,
                    listar_popup,
                    )
app_name = 'popups'
urlpatterns = [
    path('', listar_popup, name='lista_popups'),
    path('agregar/', agregar_editar, name='popup'),
    path('<int:pk>/', agregar_editar, name='popup_detalle'),
    path('delete/', eliminar_popup, name='eliminar'),
]
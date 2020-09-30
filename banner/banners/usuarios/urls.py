from django.urls import path
from .views import (home,
                    iniciar_sesion,
                    registrarse,
                    cerrar_sesion,
                    update_profile,
                    )

urlpatterns = [
    path('cerrarsesion/', cerrar_sesion, name='cerrarsesion'),
    path('iniciosesion/', iniciar_sesion, name='iniciar_sesion'),
    path('registrarse/', registrarse, name='registrarse'),
    path('perfil/', update_profile, name='perfil'),
    #path('registrarse/', update_profile, name='registrarse'),
    # path('', home, name='cerrar_sesion'),
]
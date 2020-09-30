from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from urllib.parse import urlparse
import re

from .models import Novedad
from .forms import NovedadForm

from star_ratings.models import Foo


def obtener_id_video(link):
    """
    Lo que hace es encontrar el ID del video de youtube para que luego se muestre en la página correctamente. 
   
    :param link: Tipo: string. URL del video de youtube que se quiera mostrar.
    :return: Tipo diccionario: -id correspondiente al video, -mensaje de error, -correcto en verdadero si se encontró el ID.
    """
    diccionario = {
        'id': '', 
        'mensaje': '', 
        'correcto': False
    }
    
    # esta exp regular va a verificar si el link del video cumple con el formato de youtube
    expresion_regular = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
    
    # re.search busca la cadena del segundo parametro en la exp regular, si no lo encuentra, devuelve None.
    # Que se encuentre el link en la exp reg no significa que el link sea válido. Para verificar si
    # existe este video, habría que hacer cierta conexión a youtube
    match = re.search(expresion_regular, link)
    if match is not None:
        # exp_reg_ID es una expresion para encontrar el ID del video
        exp_reg_ID = "((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)"
            
        # re.findall devuelve en una lista con una tupla de los strings que coinciden en la exp regular
        lo_que_encontro = re.findall(exp_reg_ID, link)
        for lista in lo_que_encontro:
            for item in lista:
                if len(item) > 1:
                    diccionario['id'] = item
                    diccionario['correcto'] = True
    else:
        diccionario['mensaje'] = 'Link incorrecto'

    return diccionario



def detalle(request,pk):

    return render(
        request,
        'home_copy.html',
        {
            'novedad': Novedad.objects.get(pk=pk),
            'object': (Novedad.objects.get(pk=pk)).estrellas,
        }
    )


def listar(request):
    novedades = Novedad.objects.filter(fecha_inicio__lt=timezone.now(), fecha_fin__gte=timezone.now())
    return render(
        request,
        'lista_novedades.html',
        {'novedades': novedades}
    )


@login_required
def agregar_editar(request, pk=0):
    if pk == 0:
        elemento = None
    else:
        try:
            elemento = Novedad.objects.get(pk=pk)
        except Novedad.DoesNotExist:
            mensaje = 'el elemento solicitado no existe'
            # return HttpResponseRedirect('/novedades/')
            return HttpResponseRedirect(reverse('novedades'))
    if request.POST:
        form = NovedadForm(data=request.POST, files=request.FILES, instance=elemento)
        if form.is_valid():
            # validar si imagen es jpg y no supera determinado tamaño en alto y ancho
            novedad = form.save(commit=False)
            extension = novedad.extension()
            guardar = False
            if extension == '.jpg':
                #guardar = True
                # if banner.imagen.width > 1920:
                #     guardar = False
                #     form.add_error('imagen', "Ancho máximo 1920 px")
                # if banner.imagen.height > 500:
                #     guardar = False
                #     form.add_error(
                #         'imagen',
                #         "Su imagen tiene %s px de alto. El alto máximo es de 500 px" % banner.imagen.height
                #     )
                if novedad.youtube_url != None and novedad.youtube_url != '':
                    obtener_id = obtener_id_video(novedad.youtube_url)
                    if obtener_id['correcto']:
                        novedad.youtube_video_id = obtener_id['id']
                        guardar = True
                    else:
                        form.add_error('youtube_url', obtener_id['mensaje'])
                else:
                    novedad.youtube_video_id = ""
                    guardar = True
            else:
                form.add_error('imagen', "Extensión inválida. Solo JPG")
            
            if guardar:
                novedad.usuario = request.user
                obj, created = Foo.objects.get_or_create(bar='Rating de '+novedad.titulo)
                novedad.estrellas = obj
                novedad.save()
                #return HttpResponseRedirect('/novedades/')

    else:
        form = NovedadForm(instance=elemento)

    return render(
        request,
        "agregar_editar_novedad.html",
        {
            'banners': Novedad.objects.all(),
            'form': form,
            'elemento': elemento,
        }
    )


# Eliminar banner
@login_required(login_url='/iniciosesion/')
def eliminar_novedad(request):
    if request.POST:
        pk = request.POST['pk']
        try:
            Novedad.objects.get(pk=pk).delete()
            mensaje = 'eliminado correctamente'
        except Novedad.DoesNotExist:
            mensaje = 'Elemento no encontrado'
    else:
        mensaje = 'No POST'

    return JsonResponse({
        'mensaje': mensaje,
        'url': reverse('novedades:listar_novedades'),
    })
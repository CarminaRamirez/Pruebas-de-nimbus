from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Popups
from .forms import PopupForm
from banner.views import convertir_imagen_webp


def popup(request):
    popups = Popups.objects.filter(fecha_inicio__lt=timezone.now(), fecha_fin__gte=timezone.now())
    return render(
        request,
        'Popup.html',
        {'popups': popups}
    )


@login_required(login_url='/iniciosesion/')
def listar_popup(request):

    return render(
        request,
        'lista_popups.html',
        {'popups': Popups.objects.all()}
    )


@login_required(login_url='/iniciosesion/')
# Crear y editar banner
def agregar_editar(request, pk=None):
    try:
        elemento = Popups.objects.get(pk=pk)
    except Popups.DoesNotExist:
        elemento = None
    if request.POST:
        form = PopupForm(data=request.POST, files=request.FILES, instance=elemento)
        if form.is_valid():
            # validar si imagen es jpg y no supera determinado tamaño en alto y ancho
            popup = form.save(commit=False)
            extension = popup.extension()
            guardar = False
            if extension == '.jpg':
                guardar = True
                #if popup.imagen.width > 1920:
                #    guardar = False
                #    form.add_error('imagen', "Ancho máximo 1920 px")
                #if popup.imagen.height > 500:
                #    guardar = False
                #    form.add_error(
                #        'imagen',
                #        "Su imagen tiene %s px de alto. El alto máximo es de 500 px" % popup.imagen.height
                #    )
            else:
                form.add_error('imagen', "Extensión inválida. Solo JPG")
            if guardar:
                popup.usuario = request.user
                popup.save()
                convertir_imagen_webp(es_archivo=True, imagen=popup.imagen)
                return HttpResponseRedirect('/popups/')

    else:
        form = PopupForm(instance=elemento)

    return render(
        request,
        "agregar_editar_popup.html",
        {
            'popups': Popups.objects.all(),
            'form': form,
            'elemento': elemento,
        }
    )


# Eliminar banner
@login_required(login_url='/iniciosesion/')
def eliminar_popup(request):
    if request.POST:
        pk = request.POST['pk']
        try:
            Popups.objects.get(pk=pk).delete()
            mensaje = 'eliminado correctamente'
        except Popups.DoesNotExist:
            mensaje = 'Elemento no encontrado'
    else:
        mensaje = 'No POST'

    return JsonResponse({
        'mensaje': mensaje,
        'url': reverse('popups:lista_popups'),
    })
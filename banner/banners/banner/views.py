import io
import os

from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Avg
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Banner
from .forms import BannerForm

from popups.models import Popups

from sorl.thumbnail import get_thumbnail

from PIL import Image


def home(request):
    banners = Banner.objects.filter(fecha_inicio__lt=timezone.now(), fecha_fin__gte=timezone.now())
    popups = Popups.objects.filter(fecha_inicio__lt=timezone.now(), fecha_fin__gte=timezone.now())
    return render(
                  request,
                  'home.html',
                  {'banners': banners,
                   'popups': popups,
                  }
    )


@login_required(login_url='/iniciosesion/')
def listar(request):
    return render(request,
                  'lista.html',
                  {'banners': Banner.objects.all()})


# Crear y editar banner
@login_required(login_url='/iniciosesion/')
def agregar_editar(request, pk=None):
    try:
        elemento = Banner.objects.get(pk=pk)
    except Banner.DoesNotExist:
        elemento = None
    if request.POST:
        # acá pregunto si se está editando el elemento, y se coloca una nueva imagen, 
        # se borra la anterior del almacenamiento (solamente funcionaría si hay un solo campo con un archivo)
        if elemento and request.FILES:
            default_storage.delete(elemento.imagen.path)

        form = BannerForm(data=request.POST, files=request.FILES, instance=elemento)
        if form.is_valid():
            # validar si imagen es jpg y no supera determinado tamaño en alto y ancho
            banner = form.save(commit=False)
            extension = banner.extension()
            guardar = False
            if extension == '.jpg':
                guardar = True
                if banner.imagen.width > 1920:
                    guardar = False
                    form.add_error('imagen', "Ancho máximo 1920 px")
                if banner.imagen.height > 500:
                    guardar = False
                    form.add_error(
                        'imagen',
                        "Su imagen tiene %s px de alto. El alto máximo es de 500 px" % banner.imagen.height
                    )
            else:
                form.add_error('imagen', "Extensión inválida. Solo JPG")
            if guardar:
                banner.usuario = request.user
                # banner.save()
                imagen_nueva = convertir_imagen_webp(es_archivo=False, imagen=banner.imagen)
                """ eliminar imagen previa desde el disco """
                default_storage.delete(banner.imagen.path)
                print(banner.imagen.path)
                """ actualizas modelo de datos """
                banner.imagen = imagen_nueva
                banner.save()
                return HttpResponseRedirect(reverse('banner:listar_banners'))
    else:
        form = BannerForm(instance=elemento)
        convertir_carpeta_de_imagenes_a_webp(request, path='media')

    return render(
        request,
        "agregar_editar.html",
        {
            'banners': Banner.objects.all(),
            'form': form,
            'elemento': elemento,
        }
    )


# Eliminar banner
@login_required(login_url='/iniciosesion/')
def eliminar_banner(request):
    if request.POST:
        pk = request.POST['pk']
        try:
            Banner.objects.get(pk=pk).delete()
            mensaje = 'eliminado correctamente'
        except Banner.DoesNotExist:
            mensaje = 'Elemento no encontrado'
    else:
        mensaje = 'No POST'

    return JsonResponse({
        'mensaje': mensaje,
        'url': reverse('banner:listar_banners'),
    })


def convertir_imagen_webp(es_archivo=False, imagen='', path_imagen=''):
    """
    convertir imagen desde archivo o desde upload en WEBP
    :param es_archivo: 
    :param imagen: 
    :return: 
    """

    """ identificar origen: es archivo o es upload? """
    if es_archivo:
        nombre_archivo, ext = os.path.splitext(path_imagen)
        """ abrir imagen """
        im = Image.open(path_imagen).convert("RGB")
        ruta = nombre_archivo + ".webp"
        print(ruta)
        """ convertir imagen """
        im.save(ruta, "WEBP")
        
        return ruta
    else:
        from django.core.files.uploadedfile import InMemoryUploadedFile
        nombre_archivo, ext = os.path.splitext(imagen.name)
        img = Image.open(imagen)
        thumbnailString = io.BytesIO()
        img.save(thumbnailString, 'WEBP')
        ruta = nombre_archivo + ".webp"
        newFile = InMemoryUploadedFile(thumbnailString, None, ruta, 'image/webp', thumbnailString.getbuffer().nbytes, None)
        return newFile



"""
recorrer carpeta usuario
por cada archivo JPG
llamar a la funcion creada para convertir el archivo a WEBP
eliminar archivo JPG
"""
def convertir_carpeta_de_imagenes_a_webp(request, path=''):
    """
    recorre la carpeta del path pasado por parámetro convirtiendo todos los archivos(imágenes)
    jpg a webp que contiene

    :param path: ACLARACIÓN: el path es a partir de la carpeta del proyecto (excluyendo este mismo), 
    es decir, si el proyecto se llama "nimbus" y la carpeta a la que queremos hacer referencia está en:
    nimbus
        media
            BANNERS
    entonces en el path se colocaría: media/banners
    :return: 
    """

    """si el string pasado por parámetro corresponde a un directorio, coloca en la variable
    carpeta una lista con los archivos que posee"""
    directorios_contenidos=[]
    if os.path.isdir(path):
        carpeta = os.listdir(path)
        for item in carpeta:
            """recorre la carpeta"""
            nombre_archivo, ext = os.path.splitext(item)
            """si el archivo es jpg"""
            if ext == '.jpg':
                """se concatena el path con el nombre del archivo, para formar el path del archivo"""
                path_imagen = path+'/'+item
                """se convierte el archivo"""
                nueva = convertir_imagen_webp(es_archivo=True, imagen=item, path_imagen=path_imagen)
                """para borrar el archivo jpg que ya convertimos, formamos el path absoluto para que
                la función lo encuentre"""
                path_completo = "C:\\Users\\usuario\\banner\\banners\\" + path_imagen
                default_storage.delete(path_completo)
            else:
                if ext == "":
                    path_siguiente= path+'/'+nombre_archivo
                    carpeta = os.listdir(path_siguiente)
                    for item in carpeta:
                        directorios_contenidos.append(path_siguiente)
            for dir in directorios_contenidos:
                convertir_carpeta_de_imagenes_a_webp(request=request, path=dir)
                    
                    

        
        #media/novedades/hola.webp
        #thumbnailString = io.BytesIO()
        #item.save(thumbnailString, 'jpg')
        #thumb_file = InMemoryUploadedFile(thumbnailString, None, item, 'image/jpg',
        #                                thumbnailString.getbuffer().nbytes, None)
        #print(thumb_file)
    
    #imagen_archivo = Image.new
    #print(imagen_archivo)
    #im = Image.open(imagen_archivo, 'r')
    #print(im.name)
    
    #imagen = open(imagen.path,)
    #nombre_archivo, ext = os.path.splitext(imagen)
    #if ext == '.jpg':
    #    nueva = convertir_imagen_webp(es_archivo=True, imagen=imagen)
    #    default_storage.delete(imagen_archivo)

        


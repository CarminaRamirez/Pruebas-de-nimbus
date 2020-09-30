from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import login as do_login
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from .forms import InicioSesionForm, Registrarse, ProfileForm, UserForm
from .models import Perfil


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.perfil)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            #return redirect('settings:profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.perfil)

    return render(
        request,
        'profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


def home(request):
    return render(
        request,
        'home.html',
        {}
    )


def iniciar_sesion(request):
    valuenext = request.POST.get('next')
    if request.POST:
        miFormulario = InicioSesionForm(data=request.POST)
        if miFormulario.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if valuenext:
                    return HttpResponseRedirect(valuenext)
                    print('llego al valuenext')
                else:
                    return HttpResponseRedirect('/')
            else:
                miFormulario.add_error('username', "Usuario inválido")
                print('hay un error')
        else:
            print('el form es invalido')
            print(miFormulario.data)
    else:
        miFormulario = InicioSesionForm()
        print('no paso por el post')

    return render(
        request,
        'inicio_sesion.html',
        {
            'form': miFormulario,
        }
    )


def registrarse(request):
    #form = UserCreationForm()
    form = Registrarse()
    if request.method == 'POST': #POST es como para leer y escribir, GET para leer
        #form = UserCreationForm(data=request.POST)
        form = Registrarse(data=request.POST)
        if form.is_valid():
            usuario = form.save()
            if usuario is not None:
                do_login(request, usuario)
                return HttpResponseRedirect('/')

    return render(
        request,
        'registrarse.html',
        {
            'form': form
        }
    )


def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')

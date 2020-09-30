from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Perfil


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('bio', 'direccion', 'fecha_cumple')
        widgets = {
            'fecha_cumple': DateInput,
        }


class InicioSesionForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Contraseña',
        }


class Registrarse(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        labels = {
            'username': 'Nombre de usuario',
        }
        help_texts = {
            'username': 'Ingrese 8 caracteres',
        }
        error_messages = {
            'username': {
                'max_length': 'Nombre de usuario demasiado largo.',
            },
        }
from django import forms

from .models import Popups


class DateInput(forms.DateInput):
    input_type = 'date'


class PopupForm(forms.ModelForm):

    class Meta:
        model = Popups
        fields = [
            'titulo',
            'imagen',
            'fecha_inicio',
            'fecha_fin',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Titulo del Pop up'}),
            'fecha_inicio': DateInput,
            'fecha_fin': DateInput,
        }
        labels = {
            'titulo': 'Titulo Imagen',
            'fecha_inicio': 'Fecha de inicio de publicación',
            'fecha_fin': 'Fecha de fin de publicación',
        }
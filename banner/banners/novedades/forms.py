from django import forms

from .models import Novedad


class DateInput(forms.DateInput):
    input_type = 'date'


class NovedadForm(forms.ModelForm):

    class Meta:
        model = Novedad
        fields = [
            'titulo',
            'descripcion',
            'imagen',
            'youtube_url',
            'fecha_inicio',
            'fecha_fin',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Titulo de novedad'}),
            'fecha_inicio': DateInput,
            'fecha_fin': DateInput,
            'youtube_url': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Titulo Imagen',
            'fecha_inicio': 'Fecha de inicio de publicación',
            'fecha_fin': 'Fecha de fin de publicación',
            'youtube_url': 'Video de Youtube (link)',
        }
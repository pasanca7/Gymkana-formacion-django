from django import forms
from django.forms import widgets
from .models import Event, New

class NewForm(forms.ModelForm):
    
    class Meta:
        model = New
        fields = ['title', 'subtitle', 'body', 'image']

        labels = {
            'title': 'Título',
            'subtitle': 'Subtítulo',
            'body': 'Cuerpo',
            'image': 'Imagen'
        }

    def clean_image(self):
        image = self.cleaned_data['image']

        #Case we upload the image
        if type(image) != str:
            """
            We have to check the photo format is .jpg or .png
            """
            if not (image.name.endswith('.jpg') or image.name.endswith('.png')):
                raise forms.ValidationError('El formato debe ser JPG o PNG', code = 'invalid')

            """
            We have to limit the image size to 10MB
            """
            if image.size > 10000000:
                raise forms.ValidationError('Máximo 10 MB', code = 'heavy_img')

        return image

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['title', 'subtitle', 'body', 'start_date', 'end_date']

        labels = {
            'title': 'Título',
            'subtitle': 'Subtítulo',
            'body': 'Cuerpo',
            'start_date': 'Fecha de comienzo',
            'end_date': 'Fecha de fin'
        }

        widgets = {
            'start_date': widgets.DateInput(attrs={'type':'date'}),
            'end_date': widgets.DateInput(attrs={'type':'date'}),
        }

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        """
        start_date must be before end_start
        """
        if start_date > end_date:
            raise forms.ValidationError('La fecha de comienzo no puede ser posterior a la fin', code = 'invalid_dates')

        return end_date
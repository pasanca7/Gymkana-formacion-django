from django import forms
from .models import New

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

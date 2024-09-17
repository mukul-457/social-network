from django import forms
from django.forms import ValidationError
from django.utils.text import slugify
from django.core.files.base import ContentFile
from .models import Image


import requests

class ImageCreateForm(forms.ModelForm):
    class  Meta:
        model = Image
        fields = ["title", "url", "description"]
    
    widgets = {
        'url': forms.HiddenInput
    }

    def clean_url(self):
        url = self.cleaned_data['url']
        file_format  =  url.rsplit(".", 1)[1].lower()
        if file_format not in  ["jpeg", "jpg", "png"]:
            raise ValidationError("File format of the image in URL is not supported") 
        return url
    
    def save(self, force_insert=False, force_update=False,commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        file_name = slugify(self.cleaned_data['title'])
        extension = image_url.rsplit(".",1)[1]
        image_name = f"{file_name}.{extension}"
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)
        if commit:
            image.save()
        return image
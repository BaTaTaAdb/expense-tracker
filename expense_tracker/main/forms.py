from django import forms
from main.models import Product
from PIL import Image
import requests
from io import BytesIO
from django.core.files.base import ContentFile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image_url', 'url','purchased_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'purchased_at': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'})
        }
        
    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)

        if self.cleaned_data.get('image_url'):
            image_url = self.cleaned_data['image_url']
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')  # Ensure image is in RGB mode
            img = img.resize((300, 300))  # Resize image to desired dimensions

            buffer = BytesIO()
            img.save(fp=buffer, format='JPEG')
            file_name = f"{instance.name}_compressed_gitignore.jpg"
            instance.image.save(file_name, ContentFile(buffer.getvalue()), save=False)

        if commit:
            instance.save()
        return instance

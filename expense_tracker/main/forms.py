from django import forms
from main.models import Product, OrderItem
from PIL import Image, ImageOps
import requests
from io import BytesIO
from django.core.files.base import ContentFile


class OrderFormOneItem(forms.ModelForm):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    product_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    product_image_url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    product_url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    product_purchased_at = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OrderItem
        fields = ['quantity']
        
    field_order = [
        'product_name',
        'product_price',
        'quantity'
        'product_description',
        'product_image_url',
        'product_url',
        'product_purchased_at',
    ]

    def save(self, order, commit=True):
        product = Product(
            name=self.cleaned_data['product_name'],
            price=self.cleaned_data['product_price'],
            description=self.cleaned_data['product_description'],
            image_url=self.cleaned_data['product_image_url'],
            url=self.cleaned_data['product_url'],
            purchased_at=self.cleaned_data['product_purchased_at']
        )

        # Handle the image
        if product.image_url:
            response = requests.get(product.image_url)
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')  # Ensure image is in RGB mode

            # Calculate the new size preserving the aspect ratio
            img.thumbnail((300, 300), Image.LANCZOS)

            # Create a new image with a white background
            new_img = Image.new("RGB", (300, 300), (255, 255, 255))

            # Calculate the position to paste the resized image onto the white background
            paste_position = (
                (300 - img.size[0]) // 2,
                (300 - img.size[1]) // 2
            )

            # Paste the resized image onto the white background
            new_img.paste(img, paste_position)

            # Save the new image into a buffer
            buffer = BytesIO()
            new_img.save(fp=buffer, format='JPEG')
            file_name = f"{product.name}_compressed_gitignore.jpg"
            product.image.save(file_name, ContentFile(buffer.getvalue()), save=False)

        if commit:
            product.save()

        order_item = OrderItem(
            order=order,
            product=product,
            quantity=self.cleaned_data['quantity'],
            subtotal=product.price * self.cleaned_data['quantity']
        )

        if commit:
            order_item.save()

        return order_item


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

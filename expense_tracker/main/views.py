from django.shortcuts import render, redirect
from .forms import ProductForm
from main.models import Product
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import ProductForm

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('about')  # Replace 'product_list' with your desired redirect
        else:
            print(form.errors)  # Print form errors to console for debugging
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
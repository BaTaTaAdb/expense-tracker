from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from main.models import Order, User, Product
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import ProductForm


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_details.html', {'order': order})

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

@login_required
def dashboard(request):
    orders = _get_user_orders(request)
    context = {"orders": orders, "user": request.user}
    print(context)
    return render(request, 'dashboard.html', context)


def _get_user_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return orders
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Product, CartItem


def register(request):
    if request.user.is_authenticated:
        return redirect('shop:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('shop:index')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('shop:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('shop:index')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('shop:login')


def index(request):
    if not request.user.is_authenticated:
        return redirect('shop:login')

    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('shop:login')

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('shop:index')


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('shop:login')

    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})


def update_cart(request, cart_item_id, action):
    if not request.user.is_authenticated:
        return redirect('shop:login')

    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity == 0:
            cart_item.delete()
            return redirect('shop:view_cart')
    else:
        return HttpResponseBadRequest()

    cart_item.save()
    return redirect('shop:view_cart')


def remove_from_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('shop:login')

    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('shop:view_cart')

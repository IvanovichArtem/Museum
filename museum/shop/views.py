from django.shortcuts import render, HttpResponseRedirect
from .models import ProductType, Product, ProductBasket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request, category_id=None, page=1):
    per_page = 2
    
    # Если категория указана, фильтруем товары по категории
    if category_id:
        category = ProductType.objects.get(id=category_id)
        products = Product.objects.filter(type=category)
    else:
        category = None  # Если категории нет, то фильтровать не по какой категории
        products = Product.objects.all()
    
    # Создаем пагинатор
    paginator = Paginator(products, per_page)
    
    try:
        products_paginator = paginator.page(page)
    except:
        products_paginator = paginator.page(1)  # В случае ошибок с пагинацией, по умолчанию 1-я страница
    
    # Передаем в контекст данные для отображения
    context = {
        "title": "Магазин",
        "categories": ProductType.objects.all(),
        "products": products_paginator,
        "current_category": category  # Передаем текущую категорию
    }

    return render(request, "shop/shop.html", context)


def about(request):
    context = {"title": "О магазине"}
    return render(request, "shop/about.html", context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = ProductBasket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        ProductBasket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_delete(request, basket_id):
    basket = ProductBasket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket(request):
    baskets = ProductBasket.objects.filter(user=request.user)
    
    total_cost = sum(basket.product.price * basket.quantity for basket in baskets)

    context = {
        "title": "Корзина",
        "baskets": baskets,
        "total_cost": total_cost,
    }
    return render(request, "shop/basket.html", context)
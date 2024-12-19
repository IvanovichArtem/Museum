from typing import Any
from django.shortcuts import render, HttpResponseRedirect
from .models import Exhibition, Basket, ArtPiece
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from common.views import TitleMixin
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Basket, Order
from django.http import HttpResponse
import qrcode
from io import BytesIO
    

class IndexView(TitleMixin, TemplateView):
    template_name = "catalog/index.html"
    title = "Главная"


def about(request):
    return render(request, "catalog/about.html")


def contacts(request):
    return render(request, "catalog/contacts.html")


def exhibition(request, page=1):
    # type_id = 1 -> Выставка
    exhibitions = Exhibition.objects.filter(type_id=1)
    per_page = 2
    paginator = Paginator(exhibitions, per_page)
    exhibition_paginator = paginator.page(page)

    context = {
        "title": "Выставки",
        "exhibitions": exhibition_paginator,
    }
    return render(request, "catalog/exhibition.html", context)


def events(request, page=1):
    # type_id = 2 -> Событие
    events = Exhibition.objects.filter(type_id=2)
    per_page = 2
    paginator = Paginator(events, per_page)
    events_paginator = paginator.page(page)

    context = {
        "title": "События",
        "events": events_paginator,
    }
    return render(request, "catalog/events.html", context)


@login_required
def basket_add(request, exhibition_id):
    exhibition = Exhibition.objects.get(id=exhibition_id)
    baskets = Basket.objects.filter(user=request.user, exhibition=exhibition)

    if not baskets.exists():
        Basket.objects.create(user=request.user, exhibition=exhibition, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_delete(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])



@login_required
def order_create(request):
    baskets = Basket.objects.filter(user=request.user)
    
    if not baskets.exists():
        return HttpResponse("Ваша корзина пуста.", status=400)

    order_ids = []
    
    for basket in baskets:
        order = Order.objects.create(
            user=request.user,
            exhibition=basket.exhibition,
            quantity=basket.quantity
        )
        
        order_ids.append(order.id)
        
        qr_data = ",".join(map(str, order_ids))  
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        
        img_byte_arr = BytesIO()
        img.save(img_byte_arr)
        img_byte_arr.seek(0)
        
        send_order_confirmation_email(request.user, order, img_byte_arr)
    
    baskets.delete()

    return redirect('catalog:order_success')


def send_order_confirmation_email(user, order, qr_img):
    subject = f"Подтверждение заказа №{order.id}"
    message = f"Здравствуйте, {user.username}!\n\nВаш заказ №{order.id} на выставку '{order.exhibition.name}' был успешно оформлен.\nКоличество: {order.quantity}\n\nСпасибо за использование наших услуг!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Прикрепляем QR-код к письму
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach('order_qr_code.png', qr_img.read(), 'image/png')
    email.send()

def order_success(request):
    return render(request, "catalog/order_success.html", {"title": "Заказ оформлен"})

def art_pieces(request, exhibit_id):
    art = ArtPiece.objects.get(exhibition=exhibit_id)
    return render(request, "catalog/arts.html", {"art": art, "title": Exhibition.objects.get(id=exhibit_id)})
from .views import *
from django.urls import path

app_name = "catalog"

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("about", about, name="about"),
    path("contacts", contacts, name="contacts"),
    path("exhibition", exhibition, name="exhibition"),
    path("events", events, name="events"),
    path("baskets/add/<int:exhibition_id>/", basket_add, name="basket_add"),
    path("baskets/delete/<int:basket_id>/", basket_delete, name="basket_delete"),
    path("exhibition_page/<int:page>/", exhibition, name="exhibition_paginator"),
    path("event_page/<int:page>/", events, name="event_paginator"),
    
    # Добавляем URL для оформления заказа
    path("order/create/", order_create, name="order_create"),
    path("order/success/", order_success, name="order_success"),
    path("arts/<int:exhibit_id>/", art_pieces, name="art_pieces"),
]

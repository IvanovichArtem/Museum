from django.urls import path
from .views import index, about, basket, basket_add, basket_delete

app_name = "shop"

urlpatterns = [
    path("", index, name="index"),
    path("about", about, name="about"),
    path("category/<int:category_id>/", index, name="category"),
    path("basket", basket, name="basket"),
    path("baskets/add/<int:product_id>/", basket_add, name="basket_add"),
    path("baskets/delete/<int:basket_id>/", basket_delete, name="basket_delete"),
    path("products_page/<int:page>/", index, name="products_paginator"),
]

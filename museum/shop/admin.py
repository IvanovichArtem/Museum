from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Product, ProductType, ProductBasket

@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'type') 
    search_fields = ('name', 'description')

@admin.register(ProductType)
class ProductTypeAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductBasket)
class ProductBasketAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_timestamp')
    search_fields = ('user__username', 'product__name')

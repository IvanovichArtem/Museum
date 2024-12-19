from django.contrib import admin
from .models import Exhibition, ExhibitionType, Order, Basket, ArtPiece

admin.site.register(ExhibitionType)
admin.site.register(Order)
admin.site.register(Basket)
admin.site.register(ArtPiece)

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'type', 'tickets_quantity')
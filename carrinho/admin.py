from django.contrib import admin
from .models import ItemCarrinho

@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'produto', 'quantidade')
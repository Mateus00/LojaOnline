from django.contrib import admin
from .models import Estoque, ItemEstoque, MovimentoEstoque

class ItemEstoqueInline(admin.TabularInline):
    model = ItemEstoque
    extra = 1

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)
    inlines = [ItemEstoqueInline]

@admin.register(MovimentoEstoque)
class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('estoque', 'produto', 'tipo', 'quantidade', 'data', 'usuario')
    list_filter = ('tipo', 'data', 'estoque')
    search_fields = ('produto__nome', 'estoque__nome')

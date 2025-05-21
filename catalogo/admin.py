from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco', 'categoria', 'promocao', 'preco_promocional', 'data_adicionado')
    prepopulated_fields = {"slug": ("nome",)}
    list_filter = ('categoria',)
    search_fields = ('nome',)
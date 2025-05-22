from django.contrib import admin
from .models import Categoria, Produto, Carrossel, Banner

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'promocao')
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco', 'categoria', 'banner', 'promocao', 'preco_promocional', 'data_adicionado', 'slug')
    prepopulated_fields = {"slug": ("nome",)}
    list_filter = ('categoria',)
    search_fields = ('nome',)

@admin.register(Carrossel)
class CarrosselAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria')
    
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'data_adicionado', 'slug')

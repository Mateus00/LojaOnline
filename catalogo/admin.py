from django.contrib import admin
from .models import Categoria, Produto, Carrossel, Banner
from estoque.models import Estoque, ItemEstoque

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'promocao')
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'categoria', 'preco', 'preco_promocional',
        'promocao', 'data_adicionado', 'quantidade_estoque'
    )
    prepopulated_fields = {"slug": ("nome",)}
    list_filter = ('categoria', 'promocao', 'data_adicionado')
    search_fields = ('nome', 'descricao')

    def quantidade_estoque(self, obj):
        try:
            return obj.quantidade_estoque()
        except Exception:
            return 'N/A'
    quantidade_estoque.short_description = 'Quantidade em Estoque'
    quantidade_estoque.admin_order_field = None  # evita erro de ordenação

@admin.register(Carrossel)
class CarrosselAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'promocao')
    list_filter = ('categoria', 'promocao')
    search_fields = ('titulo',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'data_adicionado')
    prepopulated_fields = {"slug": ("titulo",)}
    search_fields = ('titulo', 'descricao')

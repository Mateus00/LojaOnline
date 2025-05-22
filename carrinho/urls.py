from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.carrinho_resumo, name='ver_carrinho'),  # alterado o name aqui
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar'),
    path('adicionar-ajax/', views.adicionar_ajax, name='adicionar_ajax'),
    path('remover/<int:produto_id>/', views.remover_do_carrinho, name='remover'),
    path('atualizar/<int:produto_id>/', views.atualizar_carrinho, name='atualizar'),  # Corrigido o nome da view
]

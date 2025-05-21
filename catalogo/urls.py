# catalogo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='produtos'),
    path('<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),  # NOVA URL
]
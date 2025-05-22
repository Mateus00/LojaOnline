# catalogo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='produtos'),
    path('<slug:slug>/', views.produto_detalhe, name='produto_detalhe'),  # NOVA URL
    path('banner/<slug:slug>/', views.banner_detalhe, name='banner_detalhe'),
]
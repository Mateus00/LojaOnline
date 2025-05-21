from django.urls import path
from . import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.carrinho_view, name='carrinho'),  # 🔹 Aqui está o nome 'carrinho'
]
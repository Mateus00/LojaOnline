from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('<int:pedido_id>/', views.pedido_detalhe, name='pedido_detalhe'),
]
from django.urls import path
from . import views

app_name = "estoque"

urlpatterns = [
    path("", views.estoque_view, name="estoque_view"),
    path("movimento/", views.movimento_estoque_view, name="movimento_estoque_view"),
    path("acompanhar/", views.acompanhar_entregas, name="acompanhar_entregas"),
    path("confirmar-entrega/<int:entrega_id>/", views.confirmar_entrega, name="confirmar_entrega",),
]

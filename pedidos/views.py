from django.shortcuts import render, get_object_or_404
from .models import Pedido
from django.contrib.auth.decorators import login_required

@login_required
def pedido_detalhe(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'pedidos/pedido_detalhe.html', {'pedido': pedido})
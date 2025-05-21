from django.shortcuts import render, get_object_or_404
from .models import Produto

def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'catalogo/produto_detalhe.html', {'produto': produto})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo/lista_produtos.html', {'produtos': produtos})

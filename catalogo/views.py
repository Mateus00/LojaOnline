from django.shortcuts import render, get_object_or_404
from .models import Categoria, Produto, Banner

def produto_detalhe(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    return render(request, 'catalogo/produto_detalhe.html', {'produto': produto})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo/lista_produtos.html', {'produtos': produtos})

def banner_detalhe(request, slug):
    banner = get_object_or_404(Banner, slug=slug)
    
    carrosseis_dinamicos = []
    
    categorias_relacionadas = banner.categoria.all()

    for categoria in categorias_relacionadas:
        produtos_em_promocao = Produto.objects.filter(categoria=categoria, promocao=True)
        if produtos_em_promocao.exists():
            carrosseis_dinamicos.append({
                'titulo': categoria.nome,
                'produtos': produtos_em_promocao
            })

    context = {
        'banner': banner,
        'carrosseis_dinamicos': carrosseis_dinamicos
    }

    return render(request, 'catalogo/banner_detalhe.html', context)
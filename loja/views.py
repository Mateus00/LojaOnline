from django.shortcuts import render
from django.db.models import Sum
from catalogo.models import Produto
from carrinho.models import ItemCarrinho
from catalogo.models import Produto, Carrossel, Banner
from carrinho.models import ItemCarrinho

def carrinho_qtd(request):
    user = request.user
    if user.is_authenticated:
        total = ItemCarrinho.objects.filter(usuario=user).aggregate(total_qtd=Sum('quantidade'))['total_qtd']
        return total or 0
    return 0

def home_view(request):
    carrosseis = Carrossel.objects.all()
    carrosseis_dinamicos = []

    for carrossel in carrosseis:
        produtos = carrossel.produtos()
        if produtos.exists():
            carrosseis_dinamicos.append({
                'titulo': carrossel.titulo,
                'produtos': produtos,
            })

    contexto = {
        'carrinho_qtd': carrinho_qtd(request),  # Se preferir, fixe como 2
        'banners': Banner.objects.all(),
        'carrosseis_dinamicos': carrosseis_dinamicos,
    }
    return render(request, 'home.html', contexto)


def produtos_view(request):
    queryset = Produto.objects.all()
    q = request.GET.get('q')
    if q:
        queryset = queryset.filter(nome__icontains=q)

    contexto = {
        'produtos': queryset,
        'carrinho_qtd': carrinho_qtd(request),
    }
    return render(request, 'produtos.html', contexto)


def sobre_view(request):
    contexto = {
        'carrinho_qtd': carrinho_qtd(request),
    }
    return render(request, 'sobre.html', contexto)


def contato_view(request):
    contexto = {
        'carrinho_qtd': carrinho_qtd(request),
    }
    return render(request, 'contato.html', contexto)

from django.shortcuts import render
from django.db.models import Sum
from catalogo.models import Produto
from carrinho.models import ItemCarrinho


def carrinho_qtd(request):
    """Função auxiliar para obter quantidade total de itens no carrinho do usuário."""
    user = request.user
    if user.is_authenticated:
        total = ItemCarrinho.objects.filter(usuario=user).aggregate(total_qtd=Sum('quantidade'))['total_qtd']
        return total or 0
    return 0


def home_view(request):
    contexto = {
        #'carrinho_qtd': carrinho_qtd(request),
        'carrinho_qtd': 2,
        'produtos': Produto.objects.all()[:5],
        'produtos_promocao': Produto.objects.filter(promocao=True)
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

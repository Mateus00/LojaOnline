from django.db.models import Sum
from carrinho.models import ItemCarrinho

def carrinho_qtd(request):
    if not request.user.is_authenticated:
        return {'carrinho_qtd': 0}

    carrinho = request.session.get('carrinho', {})
    total_itens = sum(carrinho.values())
    return {'carrinho_qtd': total_itens}


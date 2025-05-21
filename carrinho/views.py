from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import ItemCarrinho


class CarrinhoMixin:
    """Adiciona a quantidade total de itens no carrinho ao contexto."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            total = ItemCarrinho.objects.filter(usuario=self.request.user).aggregate(
                total_qtd=Sum('quantidade')
            )['total_qtd']
            context['carrinho_qtd'] = total or 0
        else:
            context['carrinho_qtd'] = 0
        return context


@login_required
def carrinho_view(request):
    """View da página do carrinho de compras."""
    itens = ItemCarrinho.objects.filter(usuario=request.user)
    total = sum(item.produto.preco * item.quantidade for item in itens)
    return render(request, 'carrinho.html', {
        'itens': itens,
        'total': total
    })

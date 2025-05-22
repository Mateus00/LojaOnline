from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalogo.models import Produto


# Utilitários para sessão
def _get_carrinho(session):
    return session.get('carrinho', {})


def _save_carrinho(session, carrinho):
    session['carrinho'] = carrinho
    session.modified = True


# Adiciona um produto ao carrinho (agora exige login)
@login_required(login_url='login')
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    carrinho = _get_carrinho(request.session)
    carrinho[str(produto.id)] = carrinho.get(str(produto.id), 0) + 1
    _save_carrinho(request.session, carrinho)

    return redirect('carrinho:ver_carrinho')


@login_required(login_url='login')
def remover_do_carrinho(request, produto_id):
    carrinho = _get_carrinho(request.session)
    carrinho.pop(str(produto_id), None)
    _save_carrinho(request.session, carrinho)
    return redirect('carrinho:ver_carrinho')


@login_required(login_url='login')
def atualizar_carrinho(request, produto_id):
    if request.method == 'POST':
        try:
            quantidade = int(request.POST.get('quantidade', 1))
        except (ValueError, TypeError):
            quantidade = 1

        carrinho = _get_carrinho(request.session)
        produto_id_str = str(produto_id)

        if quantidade > 0:
            carrinho[produto_id_str] = quantidade
        else:
            carrinho.pop(produto_id_str, None)

        _save_carrinho(request.session, carrinho)

    return redirect('carrinho:ver_carrinho')


@login_required(login_url='login')
def carrinho_resumo(request):
    carrinho = _get_carrinho(request.session)
    produtos = []
    total = 0

    for produto_id_str, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id_str))
        preco = produto.preco_promocional or produto.preco
        subtotal = preco * quantidade
        total += subtotal

        produtos.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal,
        })

    context = {
        'produtos': produtos,
        'total': total,
    }

    return render(request, 'carrinho/resumo.html', context)

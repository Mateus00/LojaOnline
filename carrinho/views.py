from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalogo.models import Produto
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from urllib.parse import quote
from .utils import gerar_payload_pix, gerar_qr_code_base64
from pedidos.models import Pedido, ItemPedido
from estoque.models import Estoque, MovimentoEstoque, Entrega
from django.urls import reverse


# Utilitários para sessão
def _get_carrinho(session):
    return session.get("carrinho", {})


def _save_carrinho(session, carrinho):
    session["carrinho"] = carrinho
    session.modified = True


@require_POST
@login_required
def adicionar_ajax(request):
    produto_id = request.POST.get("produto_id")

    try:
        produto = Produto.objects.get(id=produto_id)
        carrinho = _get_carrinho(request.session)
        carrinho[str(produto.id)] = carrinho.get(str(produto.id), 0) + 1
        _save_carrinho(request.session, carrinho)
        total_itens = sum(carrinho.values())
        return JsonResponse({"status": "ok", "total_itens": total_itens})
    except Produto.DoesNotExist:
        return JsonResponse({"status": "erro", "mensagem": "Produto não encontrado"})


@login_required(login_url="login")
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = _get_carrinho(request.session)
    carrinho[str(produto.id)] = carrinho.get(str(produto.id), 0) + 1
    _save_carrinho(request.session, carrinho)
    return redirect("carrinho:ver_carrinho")


@login_required(login_url="login")
def remover_do_carrinho(request, produto_id):
    carrinho = _get_carrinho(request.session)
    carrinho.pop(str(produto_id), None)
    _save_carrinho(request.session, carrinho)
    return redirect("carrinho:ver_carrinho")


@login_required(login_url="login")
def atualizar_carrinho(request, produto_id):
    if request.method == "POST":
        try:
            quantidade = int(request.POST.get("quantidade", 1))
        except (ValueError, TypeError):
            quantidade = 1

        carrinho = _get_carrinho(request.session)
        produto_id_str = str(produto_id)

        if quantidade > 0:
            carrinho[produto_id_str] = quantidade
        else:
            carrinho.pop(produto_id_str, None)

        _save_carrinho(request.session, carrinho)

    return redirect("carrinho:ver_carrinho")


@login_required(login_url="login")
def carrinho_resumo(request):
    carrinho = _get_carrinho(request.session)
    produtos = []
    total = 0

    for produto_id_str, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id_str))
        preco = produto.preco_promocional or produto.preco
        subtotal = preco * quantidade
        total += subtotal

        produtos.append(
            {
                "produto": produto,
                "quantidade": quantidade,
                "subtotal": subtotal,
            }
        )

    context = {
        "produtos": produtos,
        "total": total,
    }

    return render(request, "carrinho/resumo.html", context)


from django.urls import reverse

@login_required(login_url="login")
@require_POST
def finalizar_compra(request):
    carrinho = _get_carrinho(request.session)
    if not carrinho:
        return redirect("carrinho:ver_carrinho")

    endereco = request.POST.get("endereco", "").strip()
    pagamento = request.POST.get("pagamento", "").strip()

    total = 0
    texto_itens = []

    estoque_padrao = Estoque.objects.first()
    estoque_em_percurso, _ = Estoque.objects.get_or_create(nome="Em Percurso")

    # ❗️Verifica estoque disponível para cada produto
    for produto_id_str, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id_str))
        item_estoque = ItemEstoque.objects.filter(estoque=estoque_padrao, produto=produto).first()
        if not item_estoque or item_estoque.quantidade < quantidade:
            return render(request, "carrinho/erro_estoque.html", {
                "produto": produto,
                "quantidade_disponivel": item_estoque.quantidade if item_estoque else 0,
                "quantidade_solicitada": quantidade,
            })

    # ✅ Criação do Pedido após confirmação de estoque
    pedido = Pedido.objects.create(usuario=request.user)

    for produto_id_str, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id_str))
        preco = produto.preco_promocional or produto.preco
        subtotal = preco * quantidade
        total += subtotal

        texto_itens.append(f"- {produto.nome} (x{quantidade}): R$ {subtotal:.2f}")

        ItemPedido.objects.create(pedido=pedido, produto=produto, quantidade=quantidade)

        MovimentoEstoque.objects.create(
            estoque=estoque_padrao,
            produto=produto,
            tipo="saida",
            quantidade=quantidade,
            usuario=request.user,
        )

        MovimentoEstoque.objects.create(
            estoque=estoque_em_percurso,
            produto=produto,
            tipo="entrada",
            quantidade=quantidade,
            usuario=request.user,
        )

        Entrega.objects.create(
            usuario=request.user, produto=produto, quantidade=quantidade
        )

    texto_final = "\n".join([
        "*Resumo do Pedido:*",
        *texto_itens,
        f"\n*Total:* R$ {total:.2f}",
        f"\n\n*Endereço de entrega:*\n{endereco}" if endereco else "",
        f"\n\n*Forma de pagamento:* {pagamento.capitalize()}",
        f"\n\n*Acompanhe seu pedido aqui:*\n{request.build_absolute_uri(reverse('pedidos:pedido_detalhe', args=[pedido.id]))}"
    ])

    whatsapp_link = f"https://wa.me/5585989747449?text={quote(texto_final)}"

    _save_carrinho(request.session, {})  # Limpa o carrinho

    if pagamento == "pix":
        payload = gerar_payload_pix("01949203301", "Minha Loja", "São Paulo", total)
        qr_code_base64 = gerar_qr_code_base64(payload)
        return render(request, "carrinho/confirmar_pix.html", {
            "qr_code": qr_code_base64,
            "pix_info": {
                "chave": "01949203301",
                "valor": f"R$ {total:.2f}",
            },
            "whatsapp_link": whatsapp_link,
        })

    return redirect(whatsapp_link)


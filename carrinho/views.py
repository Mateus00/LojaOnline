from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalogo.models import Produto
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from urllib.parse import quote
from .utils import gerar_payload_pix, gerar_qr_code_base64


# Utilitários para sessão
def _get_carrinho(session):
    return session.get('carrinho', {})


def _save_carrinho(session, carrinho):
    session['carrinho'] = carrinho
    session.modified = True


@require_POST
@login_required
def adicionar_ajax(request):
    produto_id = request.POST.get('produto_id')

    try:
        produto = Produto.objects.get(id=produto_id)
        carrinho = _get_carrinho(request.session)
        carrinho[str(produto.id)] = carrinho.get(str(produto.id), 0) + 1
        _save_carrinho(request.session, carrinho)
        total_itens = sum(carrinho.values())
        return JsonResponse({'status': 'ok', 'total_itens': total_itens})
    except Produto.DoesNotExist:
        return JsonResponse({'status': 'erro', 'mensagem': 'Produto não encontrado'})


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

@login_required(login_url='login')
@require_POST
def finalizar_compra(request):
    carrinho = _get_carrinho(request.session)
    if not carrinho:
        return redirect('carrinho:ver_carrinho')

    endereco = request.POST.get('endereco', '').strip()
    pagamento = request.POST.get('pagamento', '').strip()

    produtos = []
    total = 0
    texto_itens = []

    for produto_id_str, quantidade in carrinho.items():
        produto = get_object_or_404(Produto, id=int(produto_id_str))
        preco = produto.preco_promocional or produto.preco
        subtotal = preco * quantidade
        total += subtotal

        texto_itens.append(f"- {produto.nome} (x{quantidade}): R$ {subtotal:.2f}")

    # Texto para WhatsApp
    texto_final = "\n".join([
        "*Resumo do Pedido:*",
        *texto_itens,
        f"\n*Total:* R$ {total:.2f}",
    ])
    if endereco:
        texto_final += f"\n\n*Endereço de entrega:*\n{endereco}"
    texto_final += f"\n\n*Forma de pagamento:* {pagamento.capitalize()}"

    # WhatsApp
    numero_whatsapp = '5585989747449'
    mensagem = quote(texto_final)
    link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensagem}"

    if pagamento == 'pix':
        chave = '01949203301'
        nome = 'Minha Loja'
        cidade = 'São Paulo'
        payload = gerar_payload_pix(chave, nome, cidade, total)
        qr_code_base64 = gerar_qr_code_base64(payload)

        context = {
            'qr_code': qr_code_base64,
            'pix_info': {
                'chave': chave,
                'valor': f'R$ {total:.2f}',
            },
            'whatsapp_link': link_whatsapp
        }
        return render(request, 'carrinho/confirmar_pix.html', context)

    # Senão, redireciona direto
    request.session['carrinho'] = {}
    request.session.modified = True
    return redirect(link_whatsapp)

from django.shortcuts import render, redirect
from .models import Estoque, MovimentoEstoque
from .forms import MovimentoEstoqueForm
from django.contrib.auth.decorators import login_required

@login_required
def estoque_view(request):
    estoque = Estoque.objects.select_related('produto').all()
    return render(request, 'estoque/estoque.html', {'estoque': estoque})

@login_required
def movimento_estoque_view(request):
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            movimento = form.save(commit=False)
            movimento.usuario = request.user
            movimento.estoque = Estoque.objects.first()  # Define estoque padrão
            movimento.save()
            return redirect('estoque:estoque_view')
    else:
        form = MovimentoEstoqueForm()
    return render(request, 'estoque/movimento_estoque.html', {'form': form})

@login_required
def acompanhar_entregas(request):
    entregas = Entrega.objects.filter(usuario=request.user).select_related('produto')
    return render(request, 'estoque/acompanhar_entregas.html', {'entregas': entregas})


@login_required
def confirmar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id, usuario=request.user)
    if not entrega.entregue:
        entrega.entregue = True
        entrega.save()

        estoque_em_percurso = Estoque.objects.get(nome='Em Percurso')

        MovimentoEstoque.objects.create(
            estoque=estoque_em_percurso,
            produto=entrega.produto,
            tipo='saida',
            quantidade=entrega.quantidade,
            usuario=request.user
        )

    return redirect('estoque:acompanhar_entregas')

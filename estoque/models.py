from django.db import models
from catalogo.models import Produto
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError  # Adicione no topo

User = get_user_model()

class Estoque(models.Model):
    nome = models.CharField(max_length=100, unique=True, default="Estoque Padrão")
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class ItemEstoque(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('estoque', 'produto')

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} em {self.estoque.nome}'

class MovimentoEstoque(models.Model):
    TIPO_MOVIMENTO = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTO)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.quantidade}x {self.produto.nome} ({self.estoque.nome}) em {self.data:%d/%m/%Y}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Só age em movimentos novos
        super().save(*args, **kwargs)

        item, _ = ItemEstoque.objects.get_or_create(
            estoque=self.estoque,
            produto=self.produto
        )

        if is_new:
            if self.tipo == 'entrada':
                item.quantidade += self.quantidade
            elif self.tipo == 'saida':
                if item.quantidade < self.quantidade:
                    raise ValidationError("Estoque insuficiente para saída.")
                item.quantidade -= self.quantidade
            item.save()


class Entrega(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    entregue = models.BooleanField(default=False)

    def __str__(self):
        status = "Entregue" if self.entregue else "Em percurso"
        return f'{self.quantidade}x {self.produto.nome} - {status}'

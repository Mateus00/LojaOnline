from django.db import models
from django.conf import settings
from catalogo.models import Produto

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pendente')

    def __str__(self):
        return f"Pedido #{self.pk} - {self.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"

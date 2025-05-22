from django.db import models
from django.conf import settings
from catalogo.models import Produto

class ItemCarrinho(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'

    def get_total_preco(self):
        preco_unit = self.produto.preco_promocional or self.produto.preco
        return preco_unit * self.quantidade


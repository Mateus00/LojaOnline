from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MovimentoEstoque, ItemEstoque

@receiver(post_save, sender=MovimentoEstoque)
def atualizar_apos_movimento(sender, instance, **kwargs):
    # MovimentoEstoque já atualiza o ItemEstoque no próprio save
    pass

@receiver(post_save, sender=ItemEstoque)
def atualizar_apos_item_salvo(sender, instance, **kwargs):
    # Placeholder para lógica futura, se necessário
    pass

@receiver(post_delete, sender=ItemEstoque)
def atualizar_apos_item_deletado(sender, instance, **kwargs):
    # Placeholder para lógica futura, se necessário
    pass

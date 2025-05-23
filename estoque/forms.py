from django import forms
from .models import MovimentoEstoque

class MovimentoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentoEstoque
        fields = ['produto', 'tipo', 'quantidade']
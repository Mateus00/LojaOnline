from django import template
import re

register = template.Library()

@register.filter
def mascarar_pix(chave):
    if not chave:
        return ''

    # E-mail
    if '@' in chave:
        partes = chave.split('@')
        nome = partes[0]
        dominio = partes[1]
        if len(nome) > 2:
            nome_mascarado = nome[0] + '*' * (len(nome) - 2) + nome[-1]
        else:
            nome_mascarado = nome[0] + '*'
        return f"{nome_mascarado}@{dominio}"

    # CPF (somente dígitos)
    if re.fullmatch(r'\d{11}', chave):
        return f"{chave[:3]}.{chave[3:6]}.{chave[6:9]}-{chave[9:]}"

    # Telefone (formato brasileiro)
    if re.fullmatch(r'\d{10,11}', chave):
        if len(chave) == 11:
            return f"({chave[:2]}) {chave[2:7]}-{chave[7:]}"
        else:
            return f"({chave[:2]}) {chave[2:6]}-{chave[6:]}"
    
    # Caso não bata com nenhum padrão, retorna original
    return chave

from django.template import Library
from utils import utils


register = Library()


@register.filter
def formata_preco(val):
    return utils.formata_preco(val)


@register.filter
def carrinho_total_qtd(carrinho):
    return utils.carrinho_total_qtd(carrinho)


@register.filter
def carrinho_total(carrinho):
    return utils.carrinho_total(carrinho)
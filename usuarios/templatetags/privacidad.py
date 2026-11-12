from django import template

from usuarios.privacidad import rut_es_oculto


register = template.Library()


@register.filter
def rut_privado(value):
    return 'RUT oculto' if rut_es_oculto(value) else value

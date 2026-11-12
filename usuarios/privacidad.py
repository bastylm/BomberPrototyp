import re

from django.conf import settings


def rut_normalizado(value):
    return re.sub(r'[^0-9kK]', '', str(value or '')).upper()


def rut_es_oculto(value):
    normalized = rut_normalizado(value)
    return bool(normalized and normalized in getattr(settings, 'RUTS_OCULTOS', set()))

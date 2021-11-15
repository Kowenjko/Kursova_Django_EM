from django import template
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))


@register.filter(name='lookup')
def lookup(value, arg):
    return value[str(arg)]

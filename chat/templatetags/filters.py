from django import template

register = template.Library()

@register.filter(name='unbox_json')
def unbox_json(value, key):
    return value[key]
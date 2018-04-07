from django import template

register = template.Library()

@register.simple_tag
def tuple_key(dict, a, b):
    return dict.get((a,b))

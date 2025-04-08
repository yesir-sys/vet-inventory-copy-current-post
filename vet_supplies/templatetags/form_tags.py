from django import template
from django.utils.safestring import SafeString

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    return field

@register.filter(name='attr')
def attr(field, attr_args):
    if not hasattr(field, 'as_widget'):
        return field
        
    attr_name, attr_value = attr_args.split(':')
    return field.as_widget(attrs={attr_name: attr_value})

# templatetags/custom_staticfiles.py

from django import template
from django.templatetags.static import StaticNode

register = template.Library()

@register.tag('custom_staticfiles')
def do_staticfiles(parser, token):
    return StaticNode.handle_token(parser, token)

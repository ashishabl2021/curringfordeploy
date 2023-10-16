import os
from django import template

register = template.Library()

@register.filter
def file_exists(value):
    # Check if the file exists
    return os.path.exists(value)

from django.template import Library
from os.path import splitext

register = Library()

@register.filter(name="endswith")
def endswith(value, args):
    return any(value.lower().endswith(arg.lower()) for arg in args.split())

@register.filter(name="format")
def format(filename, max_length=40):
    name, ext = filename.rsplit('.', 1)
    if len(name) > max_length:
        return f"{name[:max_length//2]}...{name[-(max_length//2):]}.{ext}"
    return filename
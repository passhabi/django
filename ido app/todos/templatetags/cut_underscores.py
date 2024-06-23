from django import template

register = template.Library()


def cut_underscores(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, " ")


register.filter("cut_underscores", cut_underscores)


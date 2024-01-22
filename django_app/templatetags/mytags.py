from django import template

register = template.Library()

@register.simple_tag()
def beauty_number(num):
    num = str(num)
    for i in range(len(num)-3,-1,-3):
        num = num[:i] +' '+num[i:]
    return num

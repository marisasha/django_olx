from django import template
from django_app import models

register = template.Library()

@register.simple_tag()
def beauty_number(num):
    num = str(num)
    for i in range(len(num)-3,-1,-3):
        num = num[:i] +' '+num[i:]
    return num

@register.simple_tag()
def ava(user):
    user_ava = models.Profile.objects.get(user=user)
    return f"{user_ava.avatar.url}"
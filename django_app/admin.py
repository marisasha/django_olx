from django.contrib import admin
from django_app import models

# Register your models here.
admin.site.register(models.Item)
admin.site.register(models.CategoryItem)
admin.site.register(models.CommentItem)
admin.site.register(models.Room)
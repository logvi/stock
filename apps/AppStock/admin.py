__author__ = 'vitalijlogvinenko'
from django.contrib import admin
from apps.AppStock.models import Quotes, Category

admin.site.register(Category)
admin.site.register(Quotes)

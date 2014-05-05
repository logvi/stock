__author__ = 'vitalijlogvinenko'
from django.contrib import admin
from apps.AppStock.models import Quotes, Categories

admin.site.register(Categories)
admin.site.register(Quotes)

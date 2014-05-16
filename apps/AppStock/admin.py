__author__ = 'vitalijlogvinenko'
from django.contrib import admin
from apps.AppStock.models import Quotes, Category, Strategy, Ticker,  System

admin.site.register(Category)
admin.site.register(Quotes)
admin.site.register(Strategy)
admin.site.register(Ticker)
admin.site.register(System)
from django.contrib import admin
from .models import Portfolio, Stock 

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('portfolio_name', 'stocks', 'author',)

class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker',)

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Stock, StockAdmin)

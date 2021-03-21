from django import template
from stocktracker.methods import format_stock_info, due_diligence
# templatetags vs static/tags?
register = template.Library()

@register.filter(name='stocks_from_portfolio')
def stocks_from_portfolio(portfolio):
	'''
	'portfolio' would be the Portfolio model
	'''
	print('stocks_from_portfolio', portfolio.stocks)
	return format_stock_info(portfolio.stocks)

# Add the methods for turning a Portfolio into a list of stocks with all of its values
# Portfolio.objects.all(), format_stock_info, {% for stock in stocks %}
@register.filter(name='get_all_portfolios')
def get_all_porfolios(portfolios):
	for portfolio in portfolios.all():
		print(portfolio.stocks)
	return portfolios.all()

@register.filter(name='stock_due_diligence')
def stock_due_diligence(stock):
	return due_diligence(stock)

from django import template
from .methods import stocks_from_portfolio

register = template.Library()

@register.filter(name='stocks_from_portfolio')
def stocks_from_portfolio(value):
	'''
	'value' would be the Portfolio object
	'''
	return format_stock_info(value)

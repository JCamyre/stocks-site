from django import template
from stocktracker.methods import format_stock_info

register = template.Library()

@register.filter(name='stocks_from_portfolio')
def stocks_from_portfolio(value):
	'''
	'value' would be the Portfolio model
	'''
	return format_stock_info(value)
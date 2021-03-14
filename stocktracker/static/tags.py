from django import template
from .methods import stocks_from_portfolio, due_diligence

register = template.Library()

@register.filter(name='stocks_from_portfolio')
def stocks_from_portfolio(portfolio):
	'''
	'portfolio' would be the Portfolio object
	'''
	return format_stock_info(portfolio)

@register.fiter(name='stock_due_diligence')
def stock_due_diligence(stock):
	return due_diligence(stock)
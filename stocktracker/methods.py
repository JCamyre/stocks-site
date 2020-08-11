from time import sleep
import sys
# Used to access local module outside of its folder
sys.path.append('C:/Users/JWcam/Desktop/All_projects/Python-Trading')
import pytrading 
from pytrading.live_trading import trending_stocks
from pytrading.download_tickers import load_biggest_movers
from django import template

register = template.Library()

def format_stock_info(*tickers):
	stocks = []
	for stock_ticker in pytrading.Portfolio(tickers):
		stock = {}
		cur_stats = stock_ticker.df_month.iloc[-1]
		prev_stats = stock_ticker.df_month.iloc[-2]
		stock['stock_ticker'] = stock_ticker.ticker
		stock['current_price'] = cur_stats['Close']
		stock['current_percentage'] = ((cur_stats['Close'] - prev_stats['Close'])/prev_stats['Close'])*100
		stock['high_percentage'] = ((cur_stats['High'] - prev_stats['Close'])/prev_stats['Close'])*100
		stock['low_percentage'] = ((cur_stats['Low'] - prev_stats['Close'])/prev_stats['Close'])*100
		stocks.append(stock)
	return stocks


def get_trending_stocks():
	a = pytrading.Portfolio(load_biggest_movers()[:51])
	i = 0
	while True:
		if i % 10 == 0:
			a = pytrading.Portfolio(load_biggest_movers()[:51])
		trending_stocks(a)
	return stocks

# How to make the code run every 90 s

# Template filters https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#howto-custom-template-tags
# I'll do it later
@register.filter(name='stocks_from_portfolio')
def stocks_from_portfolio(value):
	'''
	'value' would be the Portfolio model
	'''
	return format_stock_info(value)


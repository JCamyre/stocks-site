from time import sleep
import py_trading as py_trd
from py_trd.live_trading import trending_stocks
from py_trd.download_tickers import load_biggest_movers
from django import template

register = template.Library()

def format_stock_info(tickers):
	stocks = []
	for stock_ticker in py_trd.Portfolio(tickers, '1m', '1d'):
		stock = {}
		cur_stats = stock_ticker.df.iloc[-1]
		stock['stock_ticker'] = stock_ticker.ticker
		stock['current_price'] = cur_stats['Close']
		stock['current_percentage'] = ((cur_stats['Close'] - stock_ticker.prev_close)/stock_ticker.prev_close)*100
		stock['high_percentage'] = ((cur_stats['High'] - stock_ticker.prev_close)/stock_ticker.prev_close)*100
		stock['low_percentage'] = ((cur_stats['Low'] - stock_ticker.prev_close)/stock_ticker.prev_close)*100
		stocks.append(stock)
	return stocks


def get_trending_stocks():
	a = py_trd.Portfolio(load_biggest_movers()[:51])
	i = 0
	while True:
		if i % 10 == 0:
			a = py_trd.Portfolio(load_biggest_movers()[:51])
		trending_stocks(a)
	return stocks

# How to make the code run every 90 s?

# Template filters https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#howto-custom-template-tags
# I'll do it later
# @register.filter(name='stocks_from_portfolio')
# def stocks_from_portfolio(value):
# 	'''
# 	'value' would be the Portfolio model
# 	'''
# 	return format_stock_info(value)


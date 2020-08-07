from django.shortcuts import render
import sys
# Used to access local module outside of its folder
sys.path.append('C:/Users/JWcam/Desktop/All_projects/Python-Trading')
from pytrading import Portfolio, Stock
from time import sleep

# Can still use the method for detecting stocks, but now it only returns the tickers, rather than printing the info for each stock
# Database?
# trending_stocks will return a list of Stock objects

def format_stock_info(*tickers):
	stocks = []
	for stock_ticker in Portfolio(tickers):
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

stocks = format_stock_info(['BNGO', 'MRNA', 'MARA', 'TAOP'])

# while True:
# 	stocks = format_stock_info(['BNGO', 'MRNA', 'MARA', 'TAOP'])
# 	print(stocks)
# 	sleep(45)

# After you login, loop through your stock tickers using format_stock_info to get the stock info on each

def home(request):
	context = {
		'stocks': stocks
	}
	return render(request, 'stocktracker/home.html', context)

def about(request):
	return render(request, 'stocktracker/about.html')


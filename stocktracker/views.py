from django.shortcuts import render
from datetime import datetime
from .methods import format_stock_info
from .models import Portfolio

# After you login, loop through your stock tickers using format_stock_info to get the stock info on each

def home(request):
	# If stocks trigger a signal, add it to the list. Updates the site every whatever time. 
	context = {
		'stocks': format_stock_info(Portfolio.objects.first().stocks),
		'yo': lambda: datetime.now().strftime('%H:%M:%S')
	}
	return render(request, 'stocktracker/home.html', context)

def about(request):
	return render(request, 'stocktracker/about.html')

# def alerts(request):
# 	context = {
# 		'stocks': format_stock_info()
# 	}

# 	return render(request, 'stocktracker/alerts.html', context)
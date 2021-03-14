from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from datetime import datetime
from .methods import format_stock_info
from .models import Portfolio, Stock

# After you login, loop through your stock tickers using format_stock_info to get the stock info on each

class PortfolioListView(ListView):
	model = Portfolio # Specify what model to be displayed 
	template_name = 'stocktracker/home.html' # Specify which template to be displayed
	context_object_name = 'portfolio' # Specify variable name to refer to model in template 'home.html'
	ordering = ['-date_posted'] # Specify the ordering of items in object, sort by descending 'date_posted'

	def get_context_data(self, **kwargs): # Creating new context objects to access in the template
		context = super().get_context_data(**kwargs)
		context['yo'] = lambda: datetime.now().strftime('%H:%M:%S') # In the template, refer to {{ yo }} to get datetime.now(). Don't have to do context.yo
		return context

class PortfolioDetailView(DetailView): # When you click on a portfolio
	model = Portfolio

class PortfolioCreateView(LoginRequiredMixin, CreateView): # Creating a portfolio
	model = Portfolio
	fields = ['portfolio_name', 'stocks']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PortfolioUpdateView(UpdateView): # Updating a portfolio
	model = Portfolio
	fields = ['portfolio_name', 'stocks']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PortfolioDeleteView(DeleteView): # Deleting a portfolio
	model = Portfolio
	success_url = '/'
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class SearchResultsView(ListView):
	model = Stock
	template_name = 'stocktracker/search_results.html'

	def get_queryset(self): # Now I can modify the returned list of stock objects
		# return Stock.objects.filter(
		# 	Q(ticker__icontains='TTM') | Q(ticker__icontains='TSM') # ticker__icontains very useful
		# )
		return Stock.objects.all()[:10]

def about(request):
	return render(request, 'stocktracker/about.html')

# def alerts(request):
# 	context = {
# 		'stocks': format_stock_info()
# 	}

# 	return render(request, 'stocktracker/alerts.html', context)
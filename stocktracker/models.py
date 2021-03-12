from django.db.models import CASCADE, CharField, ForeignKey, Model, DateTimeField
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import py_trading as py_trd
from py_trd.live_trading import get_nasdaq, get_nyse

class Portfolio(Model):
	# inherits all the methods from models.Model
	# Just store the tickers of the stocks and initialize the objects with them later
	portfolio_name = CharField(max_length=100)
	stocks = ListCharField(
		base_field = CharField(max_length=6),
		size=50,
		max_length = (50 * 11)
	)
	date_posted = DateTimeField(default=timezone.now)
	author = ForeignKey(User, on_delete=CASCADE)

	def __str__(self):
		return f'{self.portfolio_name} ({len(self.stocks)} Symbols)'

	def get_absolute_url(self):
		# go back to the urls.py, look for 'portfolio-detail', pass in the 'pk' to get the specific url with self.pk
		return reverse('portfolio-detail', kwargs={'pk': self.pk})

# The real question: Is it more efficient to set up the stocks and store them in a database. Whenever a user searches
# for a ticker, they find the object in the database and it is automatically update
# Or is it better for whenever the ticker is searched, the stock object is initialized

# I should automate creating objects for all S&P 500 + NASDAQ + NYSE
class Stock(Model):
	# Stores all information for a stock (including the due diligence)
	# Change to only ticker Charfield, then in the views search results do all the functions?
	ticker = CharField(max_length=5)

	def due_diligence(self): # Is this better than a variable named due_diligence = lambda _: stock_obj.due_diligence()
		stock_obj = py_trd.Stock(self.ticker)
		return stock_obj.due_diligence()

	def __str__(self):
		return '$' + self.ticker

	# Should I use get_absolute_url()?

"""
Do these two commands whenever you modify the models
python manage.py makemigrations
python manage.py migrate

python manage.py shell
from stocktracker.models import Portfolio
from django.contrib.auth.models import User

User.portfolio_set.create(portfolio_name='First_Portfolio', stocks=['BNGO', 'OPGN', 'NBY'])
"""

# Add all NYSE and NASDAQ tickers (S&P have stocks from these two stockmarkets)
# I think their are repeats

for ticker in get_nasdaq():
	Stock.objects.create(ticker=ticker)

for ticker in get_nyse():
	Stock.objects.create(ticker=ticker)

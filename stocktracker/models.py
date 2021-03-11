from django.db.models import CASCADE, CharField, ForeignKey, Model, DateTimeField
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import py_trading as py_trd

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

class Stock(Model):
	# Stores all information for a stock (including the due diligence)
	ticker = Charfield(max_length=5)
	due_diligence = py_trd.Stock(ticker).due_diligence()

	def __str__(self):
		return '$' + ticker

	# Should I use get_absolute_url()?

"""
Do these two commands whenever you modify the models
python manage.py makemigrations
python manage.py migrate

python manage.py shell
from stocktracker.models import Portfolio
from django.contrib.auth.models import User

user.portfolio_set.create(portfolio_name='First_Portfolio', stocks=['BNGO', 'OPGN', 'NBY'])
"""

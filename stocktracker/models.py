from django.db.models import CASCADE, CharField, ForeignKey, Model
from django_mysql.models import ListCharField
from django.contrib.auth.models import User

class Portfolio(Model):
	# inherits all the methods from models.Model
	# Just store the tickers of the stocks and initialize the objects with them later
	portfolio_name = CharField(max_length=100)
	stocks = ListCharField(
		base_field = CharField(max_length=6),
		size=50,
		max_length = (50 * 11)
	)
	author = ForeignKey(User, on_delete=CASCADE)

	def __str__(self):
		return f'{self.portfolio_name} ({len(self.stocks)} Symbols)'

"""
python manage.py makemigrations
python manage.py migrate

python manage.py shell
from stocktracker.models import Portfolio
from django.contrib.auth.models import User

user.portfolio_set.create(portfolio_name='First_Portfolio', stocks=['BNGO', 'OPGN', 'NBY'])
"""

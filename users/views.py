from django.shortcuts import render
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from stocktracker.models import Portfolio
from stocktracker.methods import format_stock_info

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form
			messages.success(request, 'Your account has been created! You are now able to log in.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	# Make sure to pass form through
	return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	current_user = request.user
	context = {
		'portfolios': current_user.portfolio_set.all(),
	}
	return render(request, 'users/profile.html', context)


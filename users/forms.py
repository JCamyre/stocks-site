from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		# Metaclasses? 
		# we are saying that we want to save the data to the User model
		model = User
		# what forms we want and this order
		fields = ['username', 'email', 'password1', 'password2']

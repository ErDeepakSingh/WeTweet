from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	username = forms.CharField(max_length=50,required=True)
	class Meta:
		model = User
		fields = ("email","username",  "password1", "password2")










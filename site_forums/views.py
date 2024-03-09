from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import LoginUser

def home(request):
	if request.user.is_authenticated:
		moderators_group = Group.objects.get(name='Moderators')
		is_mod = moderators_group.user_set.filter(id=request.user.id).exists()
		if is_mod:
			return render(request, 'home.html', {'staff':is_mod})
		else:
			return render(request, 'home.html', {'user': request.user})
	else:
		return redirect('login')
	
def login_user(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "You Have Successfully Logged In! Welcome!")
				return redirect('home')
			else:
				messages.error(request, 'There was an error with your login information. Try Again or Register!')
				return render(request, 'login.html', {'login':form})
	else:
		form = LoginForm()
		return render(request, 'login.html', {'login':form})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('profile')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'bookings/login.html')
    
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login') # replace 'login' with the name of your login url
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'bookings/profile.html')
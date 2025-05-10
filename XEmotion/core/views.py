from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages

def index(request):
    return render(request, 'index.html')
#def signin(request):
   # return render(request, 'sign-in.html')

def register(request):
    return render(request, 'registre.html')

@login_required
def chart(request):
    # Any data or logic you need to pass to the chart.html page
    return render(request, 'chart.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Standard name
        password = request.POST.get('password')  # Standard name

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('chart')  # Ensure 'chart' is defined in your urls.py
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'sign-in.html')
def logout_view(request):
    logout(request)  # This clears the session and logs out the user
    return redirect('index')  # Redirect to homepage

def about_view(request):
    return render(request, 'about.html')
def parametres_view(request):
    return render(request, 'parametres.html')

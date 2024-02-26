from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'home.html')


@login_required
def dashboard(request):
    # Get the current user
    user = request.user
    # Pass the username to the template
    return render(request, 'accounts/dashboard.html', {'username': user.username})

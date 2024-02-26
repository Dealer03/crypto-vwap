from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from html_parser.models import Transaction


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
    # Retrieve transactions associated with the current user
    user_transactions = Transaction.objects.filter(user=request.user)

    # Pass the transactions to the dashboard template
    return render(request, 'accounts/dashboard.html', {'user_transactions': user_transactions})


@login_required
def transactions(request):
    # Retrieve transactions associated with the current user
    user_transactions = Transaction.objects.filter(user=request.user)

    # Pass the transactions to the dashboard template
    return render(request, 'accounts/transactions.html', {'user_transactions': user_transactions})

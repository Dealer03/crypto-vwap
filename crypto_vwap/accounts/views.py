from django.db.models import Count, Min
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
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


def remove_duplicate_transactions(request):
    # Ensure the function is only called in response to a POST request
    if request.method == 'POST':
        # Get all transactions
        transactions = Transaction.objects.all()

        # Keep track of seen transactions based on the duplicate criteria
        seen_transactions = set()
        # List to store IDs of duplicate transactions to delete
        duplicate_ids_to_delete = []

        # Iterate over transactions and identify duplicates
        for transaction in transactions:
            # Define the key based on the specified fields
            transaction_key = (
                transaction.date,
                transaction.asset,
                transaction.average,
                transaction.filled,
                transaction.fees
            )

            # Check if this transaction is a duplicate
            if transaction_key in seen_transactions:
                # Add the ID of the duplicate transaction to delete
                duplicate_ids_to_delete.append(transaction.id)
            else:
                # Add this transaction to seen transactions
                seen_transactions.add(transaction_key)

        # Delete duplicate transactions
        num_duplicates_removed = Transaction.objects.filter(
            id__in=duplicate_ids_to_delete
        ).delete()[0]

        # Return an HTTP response with the count of deleted objects
        return HttpResponse(f"{num_duplicates_removed} duplicate transactions were removed.")
    else:
        # Return an HTTP response indicating that only POST requests are allowed
        return HttpResponse("This view only accepts POST requests.")

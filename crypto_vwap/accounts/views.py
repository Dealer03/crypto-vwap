from django.db.models import Count, Min
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from html_parser.models import Transaction

import pandas as pd
import numpy as np
import plotly.graph_objects as go


@login_required
def dashboard(request):
    # Retrieve the user's transactions
    user_transactions = Transaction.objects.filter(user=request.user)

    # Calculate total profit and loss
    total_profit_loss = sum(
        transaction.realized_profit for transaction in user_transactions)
    # Prepare data for the pie chart
    asset_labels = []
    asset_values = []
    total_portfolio_value = sum(
        transaction.filled * transaction.average for transaction in user_transactions)
    for transaction in user_transactions:
        asset_labels.append(transaction.asset)
        # Calculate percentage
        asset_values.append(transaction.filled *
                            transaction.average / total_portfolio_value * 100)

     # Create the pie chart
    fig_pie = go.Figure(
        data=[go.Pie(labels=asset_labels, values=asset_values)])
    fig_pie.update_layout(
        title='Asset Distribution',
        title_font=dict(size=24),
        title_y=1,
        title_x=0.5,
        font=dict(family='Arial', size=14),
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='right', x=1),
        margin=dict(l=20, r=20, t=80, b=20)
    )
    fig_pie.update_traces(marker=dict(
        colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))  # Custom colors

    # Prepare data for the line graph (total realized profit over time)
    dates = []
    total_realized_profit = []
    for transaction in user_transactions:
        dates.append(transaction.date)
        total_realized_profit.append(transaction.realized_profit)
    fig_line = go.Figure(data=go.Scatter(
        x=dates, y=total_realized_profit, mode='lines'))
    fig_line.update_layout(
        title='Total Realized Profit Over Time',
        title_font=dict(size=24),
        title_x=0.5,
        font=dict(family='Arial', size=14),
        xaxis=dict(title='Date'),
        yaxis=dict(title='Total Realized Profit ($)'),
        margin=dict(l=20, r=20, t=80, b=20)
    )
    # Custom color and width for line
    fig_line.update_traces(line=dict(color='#1f77b4', width=2))

    # Convert the Plotly figures to HTML
    plot_div_pie = fig_pie.to_html(full_html=False)
    plot_div_line = fig_line.to_html(full_html=False)

    # Pass the data and visualizations to the template context
    context = {
        'plot_div_pie': plot_div_pie,
        'plot_div_line': plot_div_line,
        'total_profit_loss': total_profit_loss,
    }

    return render(request, 'accounts/dashboard.html', context)


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
def transactions(request):
    sort_column = request.GET.get('sort_column', 'date')
    sort_order = request.GET.get('sort_order', 'asc')

    if sort_order == 'asc':
        sort_column = sort_column
    else:
        sort_column = '-' + sort_column

    sorted_transactions = Transaction.objects.all().order_by(sort_column)

    return render(request, 'accounts/transactions.html', {'user_transactions': sorted_transactions})


def delete_all_transactions(request):
    if request.method == 'POST':
        try:
            # Delete all transactions
            Transaction.objects.all().delete()
            # Add success message
            messages.success(
                request, 'All transactions have been deleted successfully.')
        except Exception as e:
            # Add error message
            messages.error(
                request, f'An error occurred while deleting transactions: {e}')

        # Redirect to transaction list page
        return redirect('upload_options')

    return render(request, 'delete_all_transactions.html')


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

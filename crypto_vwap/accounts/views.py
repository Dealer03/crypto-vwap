from django.db.models import Count, Min, F
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
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
        data=[go.Pie(labels=asset_labels, values=asset_values, hole=.3)])
    fig_pie.update_layout(
        title='Asset Distribution',
        paper_bgcolor='#1A1E21',
        title_font=dict(size=24, color="white"),
        title_pad_t=7,
        title_y=1,
        title_x=0.5,
        font=dict(family='Arial', size=14, color="white"),
        legend=dict(itemclick=False, orientation='v', yanchor='top',
                    y=.98, xanchor='right', x=1),
        margin=dict(l=10, r=10, t=50, b=10),
        height=575,
    )
    fig_pie.update_traces(marker=dict(
        colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))  # Custom colors

    # Prepare data for the line graph (total realized profit over time)
    dates = []
    total_realized_profit = []
    for transaction in user_transactions:
        dates.append(transaction.date)
        total_realized_profit.append(transaction.realized_profit)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=dates, y=total_realized_profit,
                             base=0,  # Base starts from 0
                             # Color based on positive/negative values
                             marker_color=[
                                 'green' if x >= 0 else 'red' for x in total_realized_profit],
                             name='Total Realized Profit'))

    fig_bar.update_layout(
        title='Total Realized Profit Over Time',
        paper_bgcolor='#1A1E21',
        plot_bgcolor='#1A1E21',
        title_font=dict(size=24, color="white"),
        title_x=0.5,
        title_pad_t=7,
        font=dict(family='Arial', size=14, color='white'),
        xaxis=dict(title='Date'),
        yaxis=dict(title='Total Realized Profit ($)'),
        margin=dict(l=20, r=20, t=80, b=20),
        height=700,
    )

    # Convert the Plotly figures to HTML
    plot_div_pie = fig_pie.to_html(full_html=False)
    plot_div_bar = fig_bar.to_html(full_html=False)

    # Truncate total_profit_loss to 2 decimal places
    truncated_profit_loss = "{:.2f}".format(total_profit_loss)

    # Comparator
    base_zero = 0.00

    # Truncate total_profit_loss to 2 decimal places
    truncated_base_zero = "{:.2f}".format(base_zero)

    # Pass the data and visualizations to the template context
    context = {
        'plot_div_pie': plot_div_pie,
        'plot_div_bar': plot_div_bar,
        'truncated_profit_loss': truncated_profit_loss,
        'truncated_base_zero': truncated_base_zero,
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


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    # Other customizations as needed


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/custom_password_reset_confirm.html'


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/custom_password_reset_complete.html'


@login_required
def transactions(request):
    sort_column = request.GET.get('sort_column', 'date')
    sort_order = request.GET.get('sort_order', 'asc')

    # Toggle the sort order
    if sort_order == 'asc':
        sort_column = sort_column
        next_sort_order = 'desc'
    else:
        sort_column = '-' + sort_column
        next_sort_order = 'asc'

    # Retrieve the sorted transactions based on the specified column and order
    sorted_transactions = Transaction.objects.all().order_by(sort_column)

    # Pass the sorted transactions and sort order to the template
    context = {
        'user_transactions': sorted_transactions,
        'sort_column': sort_column,
        'next_sort_order': next_sort_order,
    }

    return render(request, 'accounts/transactions.html', context)


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
        response = (
            "<style>"
            "body { background-color: #1A1E21; color: #ffffff; }"
            "p { margin-bottom: 10px; font-size: 30px; font-weight: bold; color: #ffffff; }"
            "</style>"
            f"<p>{num_duplicates_removed} duplicate transactions were removed.</p>"
        )
        # Return an HTTP response with the count of deleted objects
        return HttpResponse(response)
    else:
        # Return an HTTP response indicating that only POST requests are allowed
        response = (
            "<style>"
            "body { background-color: #1A1E21; color: #ffffff; }"
            "p { margin-bottom: 10px; font-size: 30px; font-weight: bold; color: #ffffff; }"
            "</style>"
            "<p>This view only accepts POST requests.</p>"
        )
    return HttpResponse(response)

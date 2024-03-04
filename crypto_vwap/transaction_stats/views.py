from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from html_parser.models import Transaction


@login_required
def holdings(request):
    # Fetch holdings data for each asset
    assets = Transaction.objects.values_list('asset', flat=True).distinct()
    holdings_data = []
    for asset in assets:
        holdings = Transaction.get_current_holdings(asset)
        weighted_average_price = Transaction.weighted_average_price(asset)
        holdings_data.append((asset, holdings, weighted_average_price))

    return render(request, 'transaction_stats/holdings.html', {'holdings_data': holdings_data})

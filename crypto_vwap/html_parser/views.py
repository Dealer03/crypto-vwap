import csv
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render

from .forms import UploadFileForm, UploadCSVFileForm
from .utils.parse import parse_html_to_csv
from .utils.import_transactions import import_transactions_from_csv
import os


def home(request):
    return render(request, 'home.html')


@login_required
def upload_options(request):
    return render(request, 'file_upload/upload_options.html')


def upload_html_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            uploaded_file = request.FILES['file']
            html_file_path = 'temp.html'
            # Save the uploaded file temporarily with .html extension
            with open(html_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Convert HTML to CSV
            csv_file = 'converted_transactions.csv'
            parse_html_to_csv('temp.html', csv_file)

            # Delete temporary HTML file
            os.remove('temp.html')

            # Modify the generated CSV file to add the 'asset' column
            modify_csv_file(csv_file)

            # Get the URL of the modified CSV file
            csv_file_url = request.build_absolute_uri(csv_file)

            # Pass the URL to the template
            return render(request, 'file_upload/html_success.html', {'csv_file_url': csv_file_url})
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/html_upload.html', {'form': form})


@login_required
def upload_csv_file(request):
    if request.method == 'POST':
        form = UploadCSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_path = './temp.csv'
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            try:
                success, error_message = import_transactions_from_csv(
                    file_path, request.user)
            except UnicodeDecodeError as e:
                error_message = str(e)
                success = False

            if success:
                return render(request, 'file_upload/csv_success.html')
            else:
                return render(request, 'file_upload/csv_upload.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadCSVFileForm()
    return render(request, 'file_upload/csv_upload.html', {'form': form})


def modify_csv_file(csv_file):
    # Function to split data in the 'quantity' column and add 'asset' column
    def split_quantity_column(data):
        parts = data.split()
        if parts:  # Check if parts is not empty
            # Assume the first part is always numeric
            quantity = float(parts[0])
            # Join the remaining parts as asset
            asset = ''.join(parts[1:]) if len(parts) > 1 else ''
        else:
            quantity = ''  # Default value if parts is empty
            asset = ''
        return quantity, asset

    # Function to remove 'usdt' from the columns
    def remove_usdt(data):
        return data.replace('USDT', '')

    # List to store modified rows
    modified_rows = []

    # Open the CSV file for reading
    with open(csv_file, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        # Convert fieldnames to list for easier manipulation
        fieldnames = list(reader.fieldnames)
        # Find the index of 'Type' column
        type_index = fieldnames.index('Type')
        # Insert 'Asset' column after 'Type' column
        fieldnames.insert(type_index + 1, 'Asset')

        # Process each row in the CSV file
        for row in reader:
            # Remove commas from specified numeric columns
            for column in ['Realized Profit', 'Volume', 'Quantity', 'Average']:
                if column in row:
                    row[column] = row[column].replace(',', '')

            quantity, asset = split_quantity_column(row['Quantity'])
            # Update the 'quantity' column with the numeric part
            row['Quantity'] = quantity
            row['Asset'] = asset  # Add the 'asset' column with the string part

            # Remove 'usdt' from 'Fee' and 'Realized Profit' columns
            row['Fee'] = remove_usdt(row['Fee'])
            row['Realized Profit'] = remove_usdt(row['Realized Profit'])
            # Remove 'usdt' from volume column
            row['Volume'] = remove_usdt(row['Volume'])

            modified_rows.append(row)

    # Open the temporary CSV file for writing
    with open('temp.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row

        # Write the modified rows to the temporary CSV file
        for row in modified_rows:
            writer.writerow(row)

    # Replace the original CSV file with the modified one
    os.replace('temp.csv', csv_file)

    print("CSV file successfully modified with the 'asset' column and 'USDT' removed from 'Fee', 'Realized Profit', and 'Volume' columns.")


def download_csv_file(request):
    file_path = os.path.join(settings.BASE_DIR, 'converted_transactions.csv')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=converted_transactions.csv'
            return response
    else:
        raise Http404("File not found")

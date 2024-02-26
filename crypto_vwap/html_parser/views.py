import csv
from django.conf import settings
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
def upload_files(request):
    if request.method == 'POST':
        html_form = UploadFileForm(request.POST, request.FILES)
        csv_form = UploadCSVFileForm(request.POST, request.FILES)

        if html_form.is_valid():
            uploaded_file = request.FILES['file']
            with open('temp.html', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            csv_file = 'converted_transactions.csv'
            parse_html_to_csv('temp.html', csv_file)
            os.remove('temp.html')

            modify_csv_file(csv_file)

            csv_file_url = request.build_absolute_uri(csv_file)
            return render(request, 'file_upload/html_success.html', {'csv_file_url': csv_file_url})

        elif csv_form.is_valid():
            uploaded_file = request.FILES['file']
            file_path = './temp.csv'
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            try:
                success, error_message = import_transactions_from_csv(
                    file_path)
            except UnicodeDecodeError as e:
                error_message = str(e)
                success = False

            if success:
                return render(request, 'file_upload/csv_success.html')
            else:
                return render(request, 'file_upload/upload_csv.html', {'csv_form': csv_form, 'error_message': error_message})

    else:
        html_form = UploadFileForm()
        csv_form = UploadCSVFileForm()

    return render(request, 'file_upload/upload_files.html', {'html_form': html_form, 'csv_form': csv_form})


@login_required
def modify_csv_file(csv_file):
    # Function to split data in the 'filled' column and add 'asset' column
    def split_filled_column(data):
        parts = data.split()
        if parts:  # Check if parts is not empty
            filled = float(parts[0])  # Assume the first part is always numeric
            # Join the remaining parts as asset
            asset = ''.join(parts[1:]) if len(parts) > 1 else ''
        else:
            filled = ''  # Default value if parts is empty
            asset = ''
        return filled, asset

    # Function to remove 'usdt' from the columns
    def remove_usdt(data):
        return data.replace('USDT', '')

    # Open the CSV file for reading and writing
    with open(csv_file, 'r', newline='') as infile, open('temp.csv', 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        # Convert fieldnames to list for easier manipulation
        fieldnames = list(reader.fieldnames)
        # Find the index of 'Type' column
        type_index = fieldnames.index('Type')
        # Insert 'Asset' column after 'Type' column
        fieldnames.insert(type_index + 1, 'Asset')

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row

        # Process each row in the CSV file
        for row in reader:
            filled, asset = split_filled_column(row['Filled'])
            # Update the 'filled' column with the numeric part
            row['Filled'] = filled
            row['Asset'] = asset  # Add the 'asset' column with the string part

            # Remove 'usdt' from 'Fees' and 'Realized Profit' columns
            row['Fees'] = remove_usdt(row['Fees'])
            row['Realized Profit'] = remove_usdt(row['Realized Profit'])

            # Write the modified row to the temporary CSV file
            writer.writerow(row)

    # Replace the original CSV file with the modified one
    os.replace('temp.csv', csv_file)

    print("CSV file successfully modified with the 'asset' column and 'usdt' removed from 'Fees' and 'Realized Profit' columns.")


@login_required
def download_csv_file(request):
    file_path = os.path.join(settings.BASE_DIR, 'converted_transactions.csv')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=converted_transactions.csv'
            return response
    else:
        raise Http404("File not found")

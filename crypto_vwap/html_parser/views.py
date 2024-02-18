import csv
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .parse import parse_html_to_csv
import os


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            uploaded_file = request.FILES['file']
            # Save the uploaded file temporarily with .html extension
            with open('temp.html', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Convert HTML to CSV
            csv_file = 'converted_transactions.csv'
            parse_html_to_csv('temp.html', csv_file)  # pass csv file path

            # Delete temporary HTML file
            os.remove('temp.html')

            # Modify the generated CSV file to add the 'asset' column
            modify_csv_file(csv_file)

            # Get the URL of the modified CSV file
            csv_file_url = request.build_absolute_uri(csv_file)

            # Pass the URL to the template
            return render(request, 'file_upload/success.html', {'csv_file_url': csv_file_url})
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/upload.html', {'form': form})


def modify_csv_file(csv_file):
    # Function to split data in the 'filled' column and add 'asset' column
    def split_filled_column(data):
        parts = data.split()
        if parts:  # Check if parts is not empty
            filled = float(parts[0])  # Assume the first part is always numeric
            # Join the remaining parts as asset
            asset = ' '.join(parts[1:]) if len(parts) > 1 else ''
        else:
            filled = ''  # Default value if parts is empty
            asset = ''
        return filled, asset

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
            # Write the modified row to the temporary CSV file
            writer.writerow(row)

    # Replace the original CSV file with the modified one
    os.replace('temp.csv', csv_file)

    print("CSV file successfully modified with the 'asset' column.")


def download_csv_file(request):
    file_path = os.path.join(settings.BASE_DIR, 'converted_transactions.csv')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=converted_transactions.csv'
            return response
    else:
        raise Http404("File not found")

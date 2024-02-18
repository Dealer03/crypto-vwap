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

            # Get the URL of the generated CSV file
            csv_file_url = request.build_absolute_uri(csv_file)

            # Pass the URL to the template
            return render(request, 'file_upload/success.html', {'csv_file_url': csv_file_url})
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/upload.html', {'form': form})


def download_csv_file(request):
    file_path = os.path.join(settings.BASE_DIR, 'converted_transactions.csv')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=converted_transactions.csv'
            return response
    else:
        raise Http404("File not found")

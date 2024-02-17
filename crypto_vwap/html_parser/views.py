from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm


def home(request):

    person = {

        "name": "Efrain Palencia",
        "age": 38,
        "gender": "Male",
    }
    return render(request, 'html_parser/home.html', {"person": person})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            uploaded_file = request.FILES['file']
            # Here you can process the uploaded file, such as saving it or parsing its content
            print(uploaded_file)
            # Once the file has been processed, redirect the user to the
            return render(request, 'file_upload/success.html')
    else:
        form = UploadFileForm()
    return render(request, 'file_upload/upload.html', {'form': form})

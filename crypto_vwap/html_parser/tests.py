# In tests.py

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UploadFileForm


class FileUploadTestCase(TestCase):
    def test_file_upload_form(self):
        # Create a file to upload
        file_content = b'Test file content'
        uploaded_file = SimpleUploadedFile('test_file.txt', file_content)

        # Post request to the file upload form view
        response = self.client.post(reverse('upload_file'), {
                                    'file': uploaded_file})

        # Check if the form submission was successful
        self.assertEqual(response.status_code, 200)

        # Check if the success template is rendered
        self.assertTemplateUsed(response, 'file_upload/success.html')

        # Optional: You can add more assertions to verify the behavior of the form submission
        # For example, you can check if the uploaded file was processed correctly

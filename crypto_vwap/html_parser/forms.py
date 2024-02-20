from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Upload'))


class UploadCSVFileForm(forms.Form):
    file = forms.FileField(label='Select s file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Upload'))

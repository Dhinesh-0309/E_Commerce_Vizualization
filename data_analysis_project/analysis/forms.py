from django import forms
from django.core.exceptions import ValidationError

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        # Check if file has a .csv extension
        if not file.name.endswith('.csv'):
            raise ValidationError("Only CSV files are allowed.")
        
        # Check if the file content type is CSV
        if file.content_type != 'text/csv':
            raise ValidationError("Uploaded file is not in CSV format.")
        
        return file

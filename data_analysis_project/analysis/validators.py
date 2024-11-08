from django.core.exceptions import ValidationError

def validate_csv_file(file):
    # Check if file extension is .csv
    if not file.name.endswith('.csv'):
        raise ValidationError("Only CSV files are allowed.")
    
    # Check MIME type to ensure it's a CSV file
    if file.content_type != 'text/csv':
        raise ValidationError("Uploaded file is not in CSV format.")

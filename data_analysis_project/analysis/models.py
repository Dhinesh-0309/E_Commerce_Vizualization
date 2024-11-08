from django.db import models
from .validators import validate_csv_file  # If you put it in a separate file

class Dataset(models.Model):
    file = models.FileField(upload_to='datasets/', validators=[validate_csv_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded at {self.uploaded_at}"

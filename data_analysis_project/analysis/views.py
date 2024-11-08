from django.shortcuts import render, redirect
from .models import Dataset
from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the file to the Dataset model
            dataset = Dataset(file=request.FILES['file'])
            dataset.full_clean()  # Validates the file
            dataset.save()

            # Perform analysis on the CSV
            file_path = dataset.file.path
            df = pd.read_csv(file_path)

            # Generate visualization
            plt.figure(figsize=(10, 6))
            df['column_of_interest'].value_counts().plot(kind='bar')
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            img_data = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()

            return render(request, 'analysis/upload.html', {
                'form': form,
                'image': img_data,
                'dataset': dataset,
            })
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})

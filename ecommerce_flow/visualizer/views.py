import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CSVUploadForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def process_file(file):
    df = pd.read_csv(file)
    df['session_duration'] = pd.to_numeric(df['session_duration'], errors='coerce')
    df.dropna(subset=['checkout_step', 'user_type', 'product_name', 'price'], inplace=True)
    return df


import pandas as pd
import plotly.express as px
import plotly.io as pio

def generate_interactive_visualizations(df):
    # List to hold the Plotly charts (as HTML)
    charts = []

    # 1. User Type Distribution
    user_type_counts = df['user_type'].value_counts().reset_index()
    user_type_counts.columns = ['User Type', 'Count']
    fig = px.bar(user_type_counts, x='User Type', y='Count', title='User Type Distribution')
    charts.append(pio.to_html(fig, full_html=False))

    # 2. Product Distribution (Top 10 Products)
    product_counts = df['product_name'].value_counts().head(10).reset_index()
    product_counts.columns = ['Product Name', 'Count']
    fig = px.bar(product_counts, x='Product Name', y='Count', title='Top 10 Products Purchased')
    charts.append(pio.to_html(fig, full_html=False))

    # 3. Category Distribution
    category_counts = df['category_name'].value_counts().reset_index()
    category_counts.columns = ['Category Name', 'Count']
    fig = px.bar(category_counts, x='Category Name', y='Count', title='Product Categories Distribution')
    charts.append(pio.to_html(fig, full_html=False))

    # 4. Payment Method Distribution
    payment_method_counts = df['payment_method'].value_counts().reset_index()
    payment_method_counts.columns = ['Payment Method', 'Count']
    fig = px.bar(payment_method_counts, x='Payment Method', y='Count', title='Payment Method Distribution')
    charts.append(pio.to_html(fig, full_html=False))

    # 5. Shipping Method Distribution
    shipping_method_counts = df['shipping_method'].value_counts().reset_index()
    shipping_method_counts.columns = ['Shipping Method', 'Count']
    fig = px.bar(shipping_method_counts, x='Shipping Method', y='Count', title='Shipping Method Distribution')
    charts.append(pio.to_html(fig, full_html=False))

    # 6. Checkout Step Distribution
    checkout_step_counts = df['checkout_step'].value_counts().sort_index().reset_index()
    checkout_step_counts.columns = ['Checkout Step', 'Count']
    fig = px.bar(checkout_step_counts, x='Checkout Step', y='Count', title='Checkout Step Distribution')
    charts.append(pio.to_html(fig, full_html=False))

    # 7. Session Duration Distribution
    fig = px.histogram(df, x='session_duration', title='Session Duration Distribution', nbins=30)
    charts.append(pio.to_html(fig, full_html=False))

    # 8. Exit Page Distribution
    exit_page_counts = df['exit_page'].value_counts().reset_index()
    exit_page_counts.columns = ['Exit Page', 'Count']
    fig = px.bar(exit_page_counts, x='Exit Page', y='Count', title='Exit Page Distribution')
    charts.append(pio.to_html(fig, full_html=False))

    # 9. Conversion Value by Product
    conversion_value_by_product = df.groupby('product_name')['conversion_value'].sum().reset_index().sort_values(by='conversion_value', ascending=False).head(10)
    fig = px.bar(conversion_value_by_product, x='product_name', y='conversion_value', title='Top 10 Products by Conversion Value')
    charts.append(pio.to_html(fig, full_html=False))

    # 10. Session Source Distribution
    session_source_counts = df['session_source'].value_counts().reset_index()
    session_source_counts.columns = ['Session Source', 'Count']
    fig = px.bar(session_source_counts, x='Session Source', y='Count', title='Session Source Distribution')
    charts.append(pio.to_html(fig, full_html=False))

    return charts


# View to handle file upload and return visualizations

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        # Process the uploaded file
        df = process_file(uploaded_file)
        
        # Generate interactive visualizations
        charts = generate_interactive_visualizations(df)
        
        # Render a response with interactive charts
        return render(request, 'visualizer/visualizations.html', {'charts': charts})

    return render(request, 'visualizer/upload.html')

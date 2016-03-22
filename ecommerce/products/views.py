from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product

class ProductDetailView(DetailView):
    model = Product

class ProductListView(ListView):
    model = Product
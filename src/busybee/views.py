from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class Rootview(TemplateView):
    template_name = "busybee/index.html"

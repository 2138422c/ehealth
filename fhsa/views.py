from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    context_dict = {'message': "Hello World"}
    return render(request, 'fhsa/index.html', context_dict)
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello world!")

#def search(request):
   # query = request.GET.get('q')
    #if query:
        #results = ...filter
    #else:
        #results = all
    #return render(request, 'results.html', {'results': results})

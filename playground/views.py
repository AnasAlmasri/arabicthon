from django.shortcuts import render

def index(request):
    index_dict = {}
    return render(request, 'index.html', context=index_dict)
    
def reader(request):
    reader_dict = {}
    return render(request, 'reader.html', context=reader_dict)

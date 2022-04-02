from django.shortcuts import render

def reader(request):
    reader_dict = {}
    return render(request, 'reader.html', context=reader_dict)

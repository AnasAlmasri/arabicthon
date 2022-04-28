import sqlite3
from django.shortcuts import render


def index(request):
    index_dict = {}
    return render(request, 'index.html', context=index_dict)


def reader(request):
    reader_dict = {}
    return render(request, 'reader.html', context=reader_dict)


def search(request):
    search_dict = {}

    if request.method == 'POST':
        search_val = request.POST['search_val']

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute(f"SELECT * FROM poem_dataset WHERE bayt LIKE '%{search_val}%' ")
        q_out = c.fetchall()
        c.close()

        search_dict = {'results': q_out}
        return render(request, 'search_results.html', context=search_dict)

    else:
        return render(request, 'search_results.html', context=search_dict)

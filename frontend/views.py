from shutil import ExecError
import sqlite3
from django.shortcuts import render


def index(request):
    index_dict = {}
    msg = ''
    try:
        if request.method == 'POST':
            
            where_clause = ''
            
            if request.POST.get('radio_poet'):
            
                # get search string
                poet_name = request.POST.get('poet_name') or None
                if poet_name is None:
                    raise Exception('Poet name is mandatory')
                                
                # construct where clause
                where_clause += f"poet LIKE '%{poet_name}%'"
            
                conn = sqlite3.connect('db.sqlite3')
                c = conn.cursor()
                c.execute(f"SELECT DISTINCT poet FROM poem_dataset WHERE {where_clause}")
                queryset = c.fetchall()
                c.close()
                
                i = 0
                poet_list = []
                row = []
                for q in queryset:
                    row.append({
                        'poet_name': q[0]
                    })
                    if len(row) == 4:
                        poet_list.append(row)
                        row = []
                    i += 1
                    if i == 8:
                        break
                    
                index_dict['poet_list'] = poet_list
                
                index_dict['search_params'] = {
                    'poet_name': poet_name
                }
                
            elif request.POST.get('radio_bayt'):
                
                # get search string
                keyword = request.POST.get('keyword') or None
                if keyword is None:
                    raise Exception('Search keyword is mandatory')
                
                # get additional parameters
                bahr = request.POST.get('bahr_dd') or None
                age = request.POST.get('age_dd') or None
                
                # construct where clause
                where_clause += f"bayt LIKE '%{keyword}%'"
                
                if bahr is not None:
                    where_clause += f" AND bahr = '{bahr}'"

                if age is not None:
                    where_clause += f" AND age = '{age}'"
                
                conn = sqlite3.connect('db.sqlite3')
                c = conn.cursor()
                c.execute(f"SELECT * FROM poem_dataset WHERE {where_clause}")
                queryset = c.fetchall()
                c.close()
                    
                index_dict['search_results'] = queryset
                
            else:
                raise Exception('Unknown search mode. Contact IT')
            
    except Exception as e:
        msg = str(e)
    
    index_dict['msg'] = msg
    
    return render(request, 'index.html', context=index_dict)


def reader(request):
    reader_dict = {}
    return render(request, 'reader.html', context=reader_dict)


def background(request):
    background_dict = {}
    return render(request, 'background.html', context=background_dict)


def library(request):
    library_dict = {}
    return render(request, 'library.html', context=library_dict)


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

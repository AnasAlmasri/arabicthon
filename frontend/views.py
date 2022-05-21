import sqlite3
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from src.poet_scraper import PoetScraper


@csrf_exempt
def ajax_poet_details(request):
    # request should be ajax and method should be POST.
    if request.method == "POST":
        poet_name = request.POST.get("poet_name")

        if poet_name:

            text = PoetScraper.search(poet_name.split(" "))

            return JsonResponse({"text": text}, status=200)

        else:

            return JsonResponse({"error": "Something went wrong!"}, status=400)


@csrf_exempt
def ajax_get_poems(request):
    # request should be ajax and method should be POST.
    if request.method == "POST":
        poet_name = request.POST.get("poet_name")

        if poet_name:

            response = []

            # construct where clause
            needle = poet_name.replace(" ", "%")

            conn = sqlite3.connect("db.sqlite3")
            c = conn.cursor()
            c.execute(
                f"SELECT shatr_left, shatr_right FROM poem_dataset WHERE poet LIKE '{needle}'"
            )
            queryset = c.fetchall()
            c.close()

            i = 0
            poem_list = []
            for q in queryset:
                poem_list.append({"shatr_left": q[0], "shatr_right": q[1]})
                i += 1
                if i == 7:
                    break

            response = poem_list

            return JsonResponse({"content": response}, status=200)

        else:

            return JsonResponse({"error": "Something went wrong!"}, status=400)


def index(request):
    index_dict = {}
    msg = ""
    try:
        if request.method == "POST":

            where_clause = ""

            if request.POST.get("radio_poet"):

                # get search string
                poet_name = request.POST.get("poet_name") or None
                if poet_name is None:
                    raise Exception("Poet name is mandatory")

                # construct where clause
                where_clause += f"poet LIKE '%{poet_name}%'"

                conn = sqlite3.connect("db.sqlite3")
                c = conn.cursor()
                c.execute(
                    f"SELECT DISTINCT poet FROM poem_dataset WHERE {where_clause}"
                )
                queryset = c.fetchall()
                c.close()

                i = 0
                poet_list = []
                row = []
                for q in queryset:
                    row.append({"poet_name": q[0]})
                    if len(row) == 4:
                        poet_list.append(row)
                        row = []
                    i += 1
                    if i == 8:
                        break

                index_dict["poet_list"] = poet_list

                index_dict["search_params"] = {"poet_name": poet_name}

            elif request.POST.get("radio_bayt"):

                # get search string
                keyword = request.POST.get("keyword") or None
                if keyword is None:
                    raise Exception("Search keyword is mandatory")

                # get additional parameters
                bahr = request.POST.get("bahr_dd") or None
                age = request.POST.get("age_dd") or None

                # construct where clause
                where_clause += f"bayt LIKE '%{keyword}%'"

                if bahr is not None:
                    where_clause += f" AND bahr = '{bahr}'"

                if age is not None:
                    where_clause += f" AND age = '{age}'"

                conn = sqlite3.connect("db.sqlite3")
                c = conn.cursor()
                c.execute(f"SELECT * FROM poem_dataset WHERE {where_clause}")
                queryset = c.fetchall()
                c.close()

                index_dict["search_results"] = queryset

            else:
                raise Exception("Unknown search mode. Contact IT")

    except Exception as e:
        msg = str(e)

    index_dict["msg"] = msg

    return render(request, "index.html", context=index_dict)


def reader(request):
    reader_dict = {}
    return render(request, "reader.html", context=reader_dict)


def background(request):
    background_dict = {}
    return render(request, "background.html", context=background_dict)


def library(request):
    library_dict = {}
    return render(request, "library.html", context=library_dict)


def search(request):
    search_dict = {}

    if request.method == "POST":
        search_val = request.POST["search_val"]

        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(f"SELECT * FROM poem_dataset WHERE bayt LIKE '%{search_val}%' ")
        q_out = c.fetchall()
        c.close()

        search_dict = {"results": q_out}
        return render(request, "search_results.html", context=search_dict)

    else:
        return render(request, "search_results.html", context=search_dict)

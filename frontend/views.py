import json
import pickle
import os
import sqlite3
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from frontend.forms import NewUserForm

# login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from src.poet_scraper import PoetScraper
from src.explainer import WordInterpretation
from sentiment_analysis.wrapper import ModelWrapper as SentimentModel
from poem_gen.wrapper import ModelWrapper as GenerationModel


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
def ajax_get_meaning(request):
    # request should be ajax and method should be POST.
    if request.method == "POST":
        word = request.POST.get("word")

        if word:

            text = WordInterpretation.get_meaning(word)

            return JsonResponse({"meaning": text}, status=200)

        else:

            return JsonResponse({"error": "Something went wrong!"}, status=400)


@csrf_exempt
def ajax_get_sentiment(request):
    # request should be ajax and method should be POST.
    if request.method == "POST":

        text = request.POST.get("text")

        if text:

            script_dir = os.path.dirname(__file__)
            rel_path = "../sentiment_analysis/models/logregmodel.pkl"
            abs_file_path = os.path.join(script_dir, rel_path)
            model = pickle.load(open(abs_file_path, "rb"))
            pred = SentimentModel.predict_logreg(text, model)

            p = "غير معروف"
            try:
                pp = pred.tolist()[0]
                if pp == 1:
                    p = "محتوى إيجابي"
                else:
                    p = "محتوى سلبي"
            except:
                pass

            return JsonResponse({"pred": p}, status=200)

        else:

            return JsonResponse({"error": "Something went wrong!"}, status=400)


@csrf_exempt
def ajax_get_prediction(request):
    # request should be ajax and method should be POST.
    if request.method == "POST":

        poet = request.POST.get("poet")
        text = request.POST.get("text")

        if text:

            pred = GenerationModel.predict_poet(poet, text)

            pred = pred.replace(poet, "")

            return JsonResponse({"pred": pred}, status=200)

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

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute(f"SELECT DISTINCT poet FROM poem_dataset order by 1")
    queryset = c.fetchall()
    c.close()

    poet_list = [{"poet_name": ""}]
    for q in queryset:
        poet_list.append({"poet_name": q[0]})

    index_dict["all_poet_dropdown"] = poet_list

    try:

        if request.method == "POST":

            where_clause = ""

            if request.POST.get("radio_poet"):

                # get search string
                poet_name = request.POST.get("poet_name") or None
                poet_dd = request.POST.get("poet_dd") or None
                if poet_name is None and poet_dd is None:
                    raise Exception("Poet name is mandatory")

                needle = poet_name
                if poet_dd:
                    needle = poet_dd

                # construct where clause
                where_clause += f"poet LIKE '%{needle}%'"

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
                    if len(queryset) <= 4:
                        if len(poet_list) == 0:
                            poet_list.append([])
                        poet_list[0].append({"poet_name": q[0]})
                    else:
                        row.append({"poet_name": q[0]})
                        if len(row) == 4:
                            poet_list.append(row)
                            row = []
                    i += 1
                    if i == 8:
                        break

                if len(poet_list) == 0:
                    raise Exception("لا توجد نتائج")

                index_dict["poet_list"] = poet_list

                index_dict["search_params"] = {"poet_name": needle}

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
                c.execute(
                    f"SELECT shatr_left, shatr_right FROM poem_dataset WHERE {where_clause}"
                )
                queryset = c.fetchall()
                c.close()

                i = 0
                poem_rows = []
                for q in queryset:
                    poem_rows.append({"shatr_left": q[0], "shatr_right": q[1]})
                    i += 1
                    if i == 7:
                        break

                if len(poem_rows) == 0:
                    raise Exception("لا توجد نتائج")

                index_dict["search_results"] = json.dumps(poem_rows)

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


def user_signup(request):
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context["signup_form"] = form
    else:
        signup_form = NewUserForm()
        context["signup_form"] = signup_form
    return render(request, "signup.html", context)


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", context={"user_auth": user})
    return render(request, "login.html", context={"user_auth": "ignore"})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def comingsoon(request):
    return render(request, "comingsoon.html", context={})

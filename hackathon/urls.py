"""hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from frontend import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("library", views.library, name="library"),
    path("poet_details/", views.ajax_poet_details, name="poet_details"),
    path("get_poems/", views.ajax_get_poems, name="get_poems"),
    path("get_meaning/", views.ajax_get_meaning, name="get_meaning"),
    path("get_sentiment/", views.ajax_get_sentiment, name="get_sentiment"),
    path("get_prediction/", views.ajax_get_prediction, name="get_prediction"),
    path("login/", views.user_login, name="login"),
    path("accounts/login/", views.user_login, name="account_login"),
    path("logout/", views.user_logout, name="logout"),
    path("signup/", views.user_signup, name="signup"),
    path("comingsoon/", views.comingsoon, name="comingsoon"),
]

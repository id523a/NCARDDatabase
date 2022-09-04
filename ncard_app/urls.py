from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path("test/show", views.CbShow.as_view(), name='fuzzy'),


    path('home', views.home, name="home"),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),


]
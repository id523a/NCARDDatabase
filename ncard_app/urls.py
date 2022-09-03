from django.urls import path

from ncard_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path("test/show",views.test_show,name='fuzzy'),
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("test/show",views.test_show,name='fuzzy'),
]
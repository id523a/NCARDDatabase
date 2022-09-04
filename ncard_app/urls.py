from django.urls import path

from . import views

app_name = 'ncard_app'

urlpatterns = [
    path('', views.index, name='index'),
    path("test/show", views.CbShow.as_view(), name='fuzzy'),
]
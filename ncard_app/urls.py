from django.urls import path

from ncard_app import views

app_name = 'ncard_app'

urlpatterns = [
    path('', views.index, name='index'),
    path("test/show",views.test_show,name='fuzzy'),
]
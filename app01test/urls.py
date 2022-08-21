from django.urls import path

from . import views

app_name = 'app01test'

urlpatterns = [
    path('', views.index, name='index'),
    path("info/", views.info_list, name='info_list'),
    path("info/ainfo", views.info_add, name='info_add'),
    path("info/<int:id>/dinfo", views.info_delete, name='info_delete'),
    path("info/<int:id>/uinfo", views.info_update, name='info_update'),
]
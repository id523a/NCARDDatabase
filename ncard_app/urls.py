from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("info/",views.info_list),
    path("info/ainfo",views.info_add),
    path("info/dinfo",views.info_delete),
    path("info/<int:id>/uinfo",views.info_update),

]
from django.urls import path

from ncard_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path("test/show",views.test_show,name='fuzzy'),
    path('tables/people', views.list_people, name="list-people"),
    path('save_people', views.save_people, name="save_people"),
]
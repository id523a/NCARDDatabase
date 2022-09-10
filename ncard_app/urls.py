from django.urls import path

from ncard_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('login_user', auth_views.LoginView.as_view(), name="login"),
    path('logout_user', auth_views.logout_then_login, name="logout"),
    path("test/show",views.test_show,name='fuzzy'),
    path('tables/people', views.list_people, name="list-people"),
    path('save_people', views.save_people, name="save_people"),
]
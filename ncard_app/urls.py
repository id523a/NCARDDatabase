from django.urls import path

from ncard_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('login_user/', auth_views.LoginView.as_view(), name="login"),
    path('logout_user/', auth_views.logout_then_login, name="logout"),
    path('tables/people/', views.list_people, name="list-people"),
    path('tables/people/add/', views.PersonDetail.as_view(), name="add-person"),
    path('tables/people/<int:id>/', views.PersonDetail.as_view(), name="edit-person"),
    
    path('save_people/', views.save_people, name="save_people"),
    
    path("test/show/",views.test_show,name='fuzzy'),
]
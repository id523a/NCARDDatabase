from django.urls import path
from ncard_app import views
from ncard_app.views.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login_user/', auth_views.LoginView.as_view(), name="login"),
    path('logout_user/', auth_views.logout_then_login, name="logout"),
    path("test/show/",views.test_show,name='fuzzy'),

    path('tables/people/', views.list_people, name="list-people"),
    path('tables/people/add/', login_required(views.PersonCreateView.as_view()), name="add-person"),
    path('tables/people/<int:pk>/', login_required(views.PersonUpdateView.as_view()), name="edit-person"),

    path('tables/organisations/', views.list_organisations, name="list-organisations"),
    path('tables/organisations/add/', login_required(views.OrganisationCreateView.as_view()), name="add-organisation"),
    path('tables/organisations/<int:pk>/', login_required(views.OrganisationUpdateView.as_view()), name="edit-organisation"),

    path('predefined/phonebook', login_required(views.PhoneBook.as_view()), name="phone_book"),
]

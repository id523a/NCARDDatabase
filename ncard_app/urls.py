from django.urls import path
from ncard_app import views
from ncard_app.views.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login_user/', auth_views.LoginView.as_view(), name="login"),
    path('logout_user/', auth_views.logout_then_login, name="logout"),
    path("test/show/",views.list_people,name='fuzzy'),

    path('tables/people/', views.FilteredPersonListView.as_view(), name="list-people"),
    path('tables/people/add/', login_required(views.PersonCreateView.as_view()), name="add-person"),
    path('tables/people/<int:pk>/', login_required(views.PersonUpdateView.as_view()), name="edit-person"),

    path('tables/organisations/', views.FilteredOrganisationListView.as_view(), name="list-organisations"),
    path('tables/organisations/add/', login_required(views.OrganisationCreateView.as_view()), name="add-organisation"),
    path('tables/organisations/<int:pk>/', login_required(views.OrganisationUpdateView.as_view()), name="edit-organisation"),

    path('tables/awards/', views.FilteredAwardListView.as_view(), name="list-awards"),
    path('tables/awards/add/', login_required(views.AwardCreateView.as_view()), name="add-award"),
    path('tables/awards/<int:pk>/', login_required(views.AwardUpdateView.as_view()), name="edit-award"),

    path('tables/events/', views.FilteredEventsListView.as_view(), name="list-events"),
    path('tables/events/add/', login_required(views.EventCreateView.as_view()), name="add-events"),
    path('tables/events/<int:pk>/', login_required(views.EventUpdateView.as_view()), name="edit-events"),

    path('predefined/phonebook', login_required(views.PhoneBook.as_view()), name="phone_book"),
    path('query/', views.custom_query, name="custom-query"),
    path('query/schema.json', views.custom_query_schema, name="custom-query-schema"),


]

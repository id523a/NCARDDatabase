from django.urls import path
from ncard_app import views
from ncard_app.views.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login_user/', auth_views.LoginView.as_view(), name="login"),
    path('logout_user/', auth_views.logout_then_login, name="logout"),

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

    path('tables/projects/', views.FilteredProjectListView.as_view(), name="list-projects"),
    path('tables/projects/add/', login_required(views.ProjectCreateView.as_view()), name="add-project"),
    path('tables/projects/<int:pk>/', login_required(views.ProjectUpdateView.as_view()), name="edit-project"),

    path('tables/grants/', views.FilteredGrantListView.as_view(), name="list-grants"),
    path('tables/grants/add/', login_required(views.GrantCreateView.as_view()), name="add-grant"),
    path('tables/grants/<int:pk>/', login_required(views.GrantUpdateView.as_view()), name="edit-grant"),

    path('tables/publications/', views.FilteredPublicationListView.as_view(), name="list-publications"),
    path('tables/publications/add/', login_required(views.PublicationCreateView.as_view()), name="add-publication"),
    path('tables/publications/<int:pk>/', login_required(views.PublicationUpdateView.as_view()), name="edit-publication"),

    path('tables/countries/', views.FilteredCountryListView.as_view(), name="list-countries"),
    path('tables/country/add/', login_required(views.CountryCreateView.as_view()), name="add-country"),
    path('tables/country/<str:pk>/', login_required(views.CountryUpdateView.as_view()),
         name="edit-country"),


    path('predefined/phonebook', login_required(views.PhoneBook.as_view()), name="phone_book"),
    path('query/', views.custom_query, name="custom-query"),
    path('query/schema.json', views.custom_query_schema, name="custom-query-schema"),


]

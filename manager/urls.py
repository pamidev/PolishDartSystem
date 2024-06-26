from django.urls import path

from manager import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    path('tournaments/', views.TournamentsListView.as_view(), name='tournaments_list'),
    path('tournaments/organizer/<int:pk>/', views.OrganizerTournamentsView.as_view(), name='organizer_tournaments'),
    path('tournaments/add/', views.TournamentAddView.as_view(), name='tournament_add'),
    path('tournaments/<int:tournament_id>/', views.tournament_details, name='tournament_details'),
    path('tournaments/<int:pk>/edit/', views.TournamentEditView.as_view(), name='tournament_edit'),

    path('tournaments/<int:tournament_id>/competitors/', views.CompetitorsListView.as_view(), name='competitors_list'),
    path('tournaments/<int:tournament_id>/competitors/<int:competitor_id>/', views.competitor_details, name='competitor'),

    path('tournaments/<int:tournament_id>/matches/', views.MatchesListView.as_view(), name='matches_list'),
    path('tournaments/<int:tournament_id>/matches/<int:pk>/edit/', views.MatchEditView.as_view(), name='match_edit'),
    path('tournaments/<int:tournament_id>/matches/add/', views.MatchAddView.as_view(), name='match_add'),

    path('dashboard/', views.dashboard, name='dashboard'),
]

from django.urls import path

from .views import TournamentsListView, HomePageView, TournamentDetailView, CompetitorsListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('tournaments/', TournamentsListView.as_view(), name='tournaments_list'),
    path('tournaments/<int:pk>/detail/', TournamentDetailView.as_view(), name='tournament_detail'),
    path('tournaments/<int:tournament_id>/competitors/', CompetitorsListView.as_view(), name='competitors_list'),
]

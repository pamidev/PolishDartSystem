from django.urls import path

from .views import CompetitorListView, MatchListView, TournamentListView

urlpatterns = [
    path('tournaments/', TournamentListView.as_view()),
    path('tournament/competitors/', CompetitorListView.as_view()),
    path('tournament/matches/', MatchListView.as_view()),
]

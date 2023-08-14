from django.urls import path

from manager import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('tournaments/', views.TournamentsListView.as_view(), name='tournaments_list'),
    path('tournaments/<int:pk>/detail/', views.TournamentDetailView.as_view(), name='tournament_detail'),
    path('tournaments/<int:tournament_id>/competitors/', views.CompetitorsListView.as_view(), name='competitors_list'),
]

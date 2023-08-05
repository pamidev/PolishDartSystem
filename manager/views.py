from django.views.generic import ListView

from .models import Tournament, Competitor, Match


class TournamentListView(ListView):
    context_object_name = 'tournament_list'
    queryset = Tournament.objects.all().order_by('-start_date')
    template_name = 'manager/tournament_list.html'


class CompetitorListView(ListView):
    context_object_name = 'competitor_list'
    queryset = (Competitor.objects.filter(is_approved=True).select_related('competitor', 'tournament'))
    template_name = 'manager/competitor_list.html'


class MatchListView(ListView):
    context_object_name = 'match_list'
    queryset = Match.objects.all().select_related('player_1', 'player_1', 'tournament').order_by('-start_date')
    template_name = 'manager/match_list.html'

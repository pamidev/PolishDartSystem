from accounts.models import CustomUser
from .models import Tournament, Competitor, Match, Training
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['num_players'] = CustomUser.objects.filter(is_player=True).count()
        context['num_judges'] = CustomUser.objects.filter(is_judge=True).count()
        context['num_organizers'] = CustomUser.objects.filter(is_organizer=True).count()
        context['num_competitors'] = Competitor.objects.filter(is_approved=True).count()
        context['num_tournaments'] = Tournament.objects.all().count()
        context['num_matches'] = Match.objects.all().count()
        context['num_trainings'] = Training.objects.all().count()

        return context


class TournamentsListView(ListView):
    context_object_name = 'tournaments_list'
    queryset = Tournament.objects.all().order_by('start_date')
    template_name = 'manager/tournaments_list.html'


class TournamentDetailView(DetailView):
    model = Tournament
    context_object_name = 'tournament_detail'
    template_name = 'manager/tournament_detail.html'


class CompetitorsListView(ListView):
    model = Competitor
    context_object_name = 'competitors_list'
    template_name = 'manager/competitors_list.html'

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return Competitor.objects.filter(tournament_id=tournament_id, is_approved=True)


class CompetitorDetailView(DetailView):
    pass


class MatchesListView(ListView):
    model = Match
    template_name = 'manager/matches_list.html'
    context_object_name = 'matches_list'

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return Match.objects.filter(tournament_id=tournament_id).select_related('player_1', 'player_2', 'tournament')


class MatchDetailView(DetailView):
    pass


class TrainingsListView(ListView):
    pass


class TrainingDetailView(DetailView):
    pass


# @method_decorator(login_required, name='dispatch')
# class SetApprovalStatusView(View):
#
#     def post(self, request, *args, **kwargs):
#         tournament_id = kwargs['tournament_id']
#         competitor_id = kwargs['competitor_id']
#
#         tournament = get_object_or_404(Tournament, id=tournament_id)
#
#         if not request.user.is_superuser and tournament.organizer != request.user:
#             return HttpResponseForbidden("Nie masz uprawnień do zarządzania tym turniejem.")
#
#         competitor = get_object_or_404(Competitor, id=competitor_id, tournament_id=tournament_id)
#
#         is_approved = request.POST.get('is_approved', False)
#         competitor.is_approved = bool(is_approved)
#         competitor.save()
#
#         return redirect('competitors_list', tournament_id=tournament_id)

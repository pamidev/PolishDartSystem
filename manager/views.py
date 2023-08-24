from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Case, When, Value, BooleanField
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView

from accounts.models import CustomUser
from .forms import TournamentForm, CompetitorForm
from .models import Tournament, Competitor, Match, Training


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['num_players'] = Competitor.objects.filter(is_player=True).count()
        context['num_judges'] = Competitor.objects.filter(is_judge=True).count()
        context['num_organizers'] = CustomUser.objects.filter(is_organizer=True).count()
        context['num_tournaments'] = Tournament.objects.all().count()
        context['num_matches'] = Match.objects.all().count()
        context['num_trainings'] = Training.objects.all().count()

        return context


@login_required()
def dashboard(request):
    tournament = get_object_or_404(Tournament, pk=request.user.id)
    is_registered = False
    user = request.user

    tournaments_as_player = Tournament.objects.filter(
        competitor__competitor=user,
        competitor__competitor__is_player=True
    ).distinct().order_by('start_date')

    tournaments_as_judge = Tournament.objects.filter(
        competitor__competitor=user,
        competitor__competitor__is_judge=True
    ).distinct().order_by('start_date')

    tournaments_as_organizer = Tournament.objects.filter(
        competitor__competitor=user,
        competitor__competitor__is_organizer=True,
        organizer=user
    ).distinct().order_by('start_date')

    matches_as_player = Match.objects.filter(
        Q(player_1__competitor=user) | Q(player_2__competitor=user),
        player_1__competitor__is_player=True
    ).annotate(
        is_player_match=Case(
            When(player_1__competitor=user, then=Value(True)),
            When(player_2__competitor=user, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).filter(is_player_match=True).select_related('player_1__competitor')

    matches_as_judge = Match.objects.filter(
        judge__competitor=user,
        judge__competitor__is_judge=True
    ).distinct()

    if request.user.is_authenticated:
        is_registered = tournament.competitor_set.filter(competitor=request.user).exists()

    context = {
        'tournaments_as_player': tournaments_as_player,
        'tournaments_as_judge': tournaments_as_judge,
        'tournaments_as_organizer': tournaments_as_organizer,
        'matches_as_player': matches_as_player,
        'matches_as_judge': matches_as_judge,
        'is_registered': is_registered,
    }

    return render(request, 'manager/dashboard.html', context)


class TournamentAddView(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'manager/tournament_add.html'
    success_url = reverse_lazy('tournaments_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class TournamentEditView(LoginRequiredMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'manager/tournament_edit.html'
    context_object_name = 'tournament_edit'

    def get_success_url(self):
        return reverse('tournaments', kwargs={'pk': self.object.pk})


class TournamentsListView(ListView):
    model = Tournament
    context_object_name = 'tournaments_list'
    template_name = 'manager/tournaments_list.html'
    ordering = 'start_date'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            players=Count('competitor', filter=Q(competitor__is_player=True))
        )
        return queryset


def is_tournament_organizer(user):
    return Tournament.objects.filter(organizer=user).exists()


@method_decorator(user_passes_test(is_tournament_organizer), name='dispatch')
class OrganizerTournamentsView(ListView):
    model = Tournament
    context_object_name = 'organizer_tournaments'
    template_name = 'manager/organizer_tournaments.html'
    ordering = 'start_date'

    def get_queryset(self):
        user = self.request.user
        return Tournament.objects.filter(organizer=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournaments = context['organizer_tournaments']

        for tournament in tournaments:
            competitors = Competitor.objects.filter(tournament=tournament).count()
            tournament.competitors = competitors

        return context


@login_required
def tournament_details(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    is_registered = False

    if request.user.is_authenticated:
        is_registered = tournament.competitor_set.filter(competitor=request.user).exists()

    if request.method == 'POST':
        form = CompetitorForm(request.POST)
        if form.is_valid():
            competitor = form.save(commit=False)
            competitor.competitor = request.user
            competitor.tournament = tournament
            competitor.joined = timezone.now()
            competitor.save()

            messages.success(request, 'You have been successfully added as a competitor.')

            return redirect('tournament_details', tournament_id=tournament_id)
    else:
        form = CompetitorForm()

    num_all_competitors = Competitor.objects.filter(tournament=tournament).count()
    num_players = Competitor.objects.filter(tournament=tournament, is_player=True).count()
    num_judges = Competitor.objects.filter(tournament=tournament, is_judge=True).count()
    is_player = Competitor.objects.filter(tournament=tournament, competitor=request.user, is_player=True).exists()
    is_judge = Competitor.objects.filter(tournament=tournament, competitor=request.user, is_judge=True).exists()
    is_organizer = Tournament.objects.filter(organizer=request.user).exists()

    context = {
        'tournament': tournament,
        'form': form,
        'num_all_competitors': num_all_competitors,
        'num_players': num_players,
        'num_judges': num_judges,
        'is_registered': is_registered,
        'is_player': is_player,
        'is_judge': is_judge,
        'is_organizer': is_organizer,
    }

    return render(request, 'manager/tournament_details.html', context)


class CompetitorsListView(ListView):
    model = Competitor
    context_object_name = 'competitors_list'
    template_name = 'manager/competitors_list.html'

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return Competitor.objects.filter(tournament_id=tournament_id, is_player=True)


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

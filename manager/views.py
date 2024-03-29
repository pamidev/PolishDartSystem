from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Case, When, Value, BooleanField
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView

from accounts.models import CustomUser
from .forms import TournamentForm, CompetitorForm, MatchForm
from .models import Tournament, Competitor, Match, Training, MatchType


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['num_players'] = Competitor.objects.filter(is_player=True).values('competitor').distinct().count()
        context['num_judges'] = Competitor.objects.filter(is_judge=True).values('competitor').distinct().count()
        context['num_organizers'] = CustomUser.objects.filter(is_organizer=True).distinct().count()
        context['num_tournaments'] = Tournament.objects.all().count()
        context['num_matches'] = Match.objects.all().count()
        context['num_trainings'] = Training.objects.all().count()

        return context


@login_required
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


class TournamentEditView(LoginRequiredMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'manager/tournament_edit.html'
    context_object_name = 'tournament_edit'

    def form_valid(self, form):
        tournament_name_exists = Tournament.objects.filter(name=form.instance.name).exists()

        if tournament_name_exists and form.instance.name != self.object.name:
            return messages.error(self.request, "This tournament name already exists.")

        form.instance.edited = datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournament_details', kwargs={'tournament_id': self.object.pk})


class TournamentsListView(ListView):
    model = Tournament
    context_object_name = 'tournaments_list'
    template_name = 'manager/tournaments_list.html'
    ordering = 'start_date'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            players=Count('competitor', filter=Q(competitor__is_player=True)),
            judges=Count('competitor', filter=Q(competitor__is_judge=True)),
        )
        return queryset


class OrganizerTournamentsView(LoginRequiredMixin, ListView):
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

    if request.method == 'POST':
        form = CompetitorForm(request.POST)
        if form.is_valid():
            if Competitor.objects.filter(tournament=tournament, competitor=request.user).exists():
                messages.error(request, 'You are already registered in this tournament.')
            elif request.user.is_superuser:
                messages.error(request, 'As a superuser You cannot be registered in any tournament.')
            else:
                competitor = form.save(commit=False)
                competitor.competitor = request.user
                competitor.tournament = tournament
                competitor.joined = datetime.now()
                competitor.save()

                messages.success(request, 'You have been successfully registered.')

            return redirect('tournament_details', tournament_id=tournament_id)
    else:
        form = CompetitorForm()

    num_registered = Competitor.objects.filter(tournament=tournament).count()
    num_players = Competitor.objects.filter(tournament=tournament, is_player=True).count()
    num_judges = Competitor.objects.filter(tournament=tournament, is_judge=True).count()
    is_registered = Competitor.objects.filter(tournament=tournament, competitor=request.user).exists()
    is_player = Competitor.objects.filter(tournament=tournament, competitor=request.user, is_player=True).exists()
    is_judge = Competitor.objects.filter(tournament=tournament, competitor=request.user, is_judge=True).exists()
    is_tournament_organizer = tournament.organizer == request.user

    context = {
        'tournament': tournament,
        'form': form,
        'num_registered': num_registered,
        'num_players': num_players,
        'num_judges': num_judges,
        'is_registered': is_registered,
        'is_player': is_player,
        'is_judge': is_judge,
        'is_tournament_organizer': is_tournament_organizer,
    }

    return render(request, 'manager/tournament_details.html', context)


class CompetitorsListView(ListView):
    model = Competitor
    context_object_name = 'competitors_list'
    template_name = 'manager/competitors_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament_id = self.kwargs['tournament_id']

        tournament = get_object_or_404(Tournament, pk=tournament_id)

        approved_competitors = (Competitor.objects.filter(tournament=tournament, is_player=True) |
                                Competitor.objects.filter(tournament=tournament, is_judge=True))

        all_competitors = Competitor.objects.filter(tournament=tournament)

        for competitor in approved_competitors:
            competitor.is_player = competitor.is_player and competitor.tournament_id == tournament_id
            competitor.is_judge = competitor.is_judge and competitor.tournament_id == tournament_id

        context.update({
            'tournament': tournament,
            'competitors_list': all_competitors,
            'approved_competitors': approved_competitors,
        })

        return context


@login_required
def competitor_details(request, tournament_id, competitor_id):
    competitor = get_object_or_404(Competitor, pk=competitor_id)
    tournament = competitor.tournament

    if request.method == 'POST':
        form = CompetitorForm(request.POST, instance=competitor)

        if form.is_valid():
            competitor = form.save(commit=False)
            competitor.is_player = form.cleaned_data['is_player']
            competitor.is_judge = form.cleaned_data['is_judge']
            competitor.edited = datetime.now()
            competitor.save()

            messages.success(request, 'Successfully updated.')

        return redirect('competitors_list', tournament_id=tournament_id)
    else:
        form = CompetitorForm(instance=competitor)

    context = {
        'competitor': competitor,
        'tournament': tournament,
        'form': form,
    }

    return render(request, 'manager/competitor_details.html', context)


class MatchAddView(LoginRequiredMixin, CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'manager/match_add.html'

    def get_success_url(self):
        if 'tournament_id' in self.kwargs:
            return reverse('matches_list', kwargs={'tournament_id': self.kwargs['tournament_id']})
        else:
            return reverse('tournaments_list')

    def get_queryset(self):
        return Tournament.objects.filter(organizer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournaments = self.get_queryset()
        context['tournaments'] = tournaments
        if 'tournament_id' in self.kwargs:
            tournament_id = self.kwargs['tournament_id']
            context['tournament_players'] = Competitor.objects.filter(tournament_id=tournament_id, is_player=True)
            context['tournament_judges'] = Competitor.objects.filter(tournament_id=tournament_id, is_judge=True)
            context['match_types'] = MatchType.objects.all()
        return context


class MatchesListView(ListView):
    model = Match
    template_name = 'manager/matches_list.html'
    context_object_name = 'matches_list'

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return Match.objects.filter(tournament_id=tournament_id).select_related('player_1', 'player_2', 'tournament')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament_id = self.kwargs['tournament_id']
        tournament = Tournament.objects.get(pk=tournament_id)
        context['tournament'] = tournament
        return context


class MatchEditView(LoginRequiredMixin, UpdateView):
    model = Match
    form_class = MatchForm
    template_name = 'manager/match_edit.html'
    context_object_name = 'match_edit'

    def get_success_url(self):
        return reverse('matches_list')


class MatchDetailView(DetailView):
    pass


class TrainingsListView(ListView):
    pass


class TrainingDetailView(DetailView):
    pass

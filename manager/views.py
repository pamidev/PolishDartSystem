from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Case, When, Value, BooleanField
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView

from accounts.models import CustomUser
from .forms import TournamentForm, CompetitorForm
from .models import Tournament, Competitor, Match, Training


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['num_players'] = CustomUser.objects.filter(is_player=True).count()
        context['num_judges'] = CustomUser.objects.filter(is_judge=True).count()
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

    is_approved = Competitor.objects.filter(tournament=tournament, is_approved=True, competitor=request.user)

    context = {
        'tournaments_as_player': tournaments_as_player,
        'tournaments_as_judge': tournaments_as_judge,
        'tournaments_as_organizer': tournaments_as_organizer,
        'matches_as_player': matches_as_player,
        'matches_as_judge': matches_as_judge,
        'is_approved': is_approved,
        'is_registered': is_registered,
    }

    return render(request, 'manager/dashboard.html', context)


class CompetitorsMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            approved_competitors=Count('competitor', filter=Q(competitor__is_approved=True))
        )
        return queryset


class TournamentAddView(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'manager/tournament_add.html'
    success_url = reverse_lazy('tournaments_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class TournamentEditView(LoginRequiredMixin, UpdateView):
    form_class = TournamentForm
    template_name = 'manager/tournament_edit.html'
    success_url = reverse_lazy('tournaments_list')


class TournamentsListView(CompetitorsMixin, ListView):
    model = Tournament
    context_object_name = 'tournaments_list'
    template_name = 'manager/tournaments_list.html'
    ordering = 'start_date'


@login_required
def tournament_details(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    is_registered = False
    has_required_profile_fields = all(
        getattr(request.user, field_name, None) for field_name in ['first_name', 'last_name', 'email']
    )

    if request.user.is_authenticated:
        is_registered = tournament.competitor_set.filter(competitor=request.user).exists()

    if request.method == 'POST':
        if has_required_profile_fields:
            form = CompetitorForm(request.POST)
            if form.is_valid():
                competitor = form.save(commit=False)
                competitor.competitor = request.user
                competitor.tournament = tournament
                competitor.save()

                messages.success(request, 'You have been successfully added as a competitor.')

                return redirect('tournament_details', tournament_id=tournament_id)
        else:
            missing_fields = [field_name for field_name in ['first_name', 'last_name', 'email']
                              if not getattr(request.user, field_name, None)]
            context = {
                'tournament': tournament,
                'missing_fields': missing_fields,
            }
            return render(request, 'manager/tournament_details.html', context)
    else:
        form = CompetitorForm()

    all_competitors = Competitor.objects.filter(tournament=tournament).count()
    approved_competitors = Competitor.objects.filter(tournament=tournament, is_approved=True).count()
    is_approved = Competitor.objects.filter(tournament=tournament, is_approved=True, competitor=request.user)

    context = {
        'tournament': tournament,
        'form': form,
        'all_competitors': all_competitors,
        'approved_competitors': approved_competitors,
        'is_registered': is_registered,
        'is_approved': is_approved,
        'has_required_profile_fields': has_required_profile_fields,
    }

    return render(request, 'manager/tournament_details.html', context)


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

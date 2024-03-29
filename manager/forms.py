from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Competitor, Friend, Match, MatchType, Training, Tournament


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = [
            'name',
            'start_date',
            'end_date',
            'place',
            'country',
            'city',
            'address',
        ]


class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = [
            'tournament',
            'match_type',
            'player_1',
            'player_2',
            'judge',
        ]

    def clean(self):
        cleaned_data = super().clean()
        player_1 = cleaned_data.get('player_1')
        player_2 = cleaned_data.get('player_2')
        judge = cleaned_data.get('judge')

        if player_1 == player_2 or player_1 == judge or player_2 == judge:
            raise ValidationError("Player 1, Player 2, and Judge must be unique person.")


class CompetitorForm(ModelForm):
    class Meta:
        model = Competitor
        fields = []

        competitor = forms.IntegerField(widget=forms.HiddenInput())
        tournament = forms.IntegerField(widget=forms.HiddenInput())

    is_player = forms.BooleanField(label='Player', required=False)
    is_judge = forms.BooleanField(label='Judge', required=False)


class FriendForm(ModelForm):
    class Meta:
        model = Friend
        fields = [
            'buddy_with',
            'name',
        ]


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = [
            'player_1',
            'player_2',
            'match_type',
        ]


class MatchTypeForm(ModelForm):
    class Meta:
        model = MatchType
        fields = [
            'game_type',
            'name',
            'sets',
            'legs',
        ]

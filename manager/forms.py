from django.forms import Form

from .models import Competitor, Friend, Match, MatchType, Training, Tournament


class TournamentCreationForm(Form):
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


class MatchCreationForm(Form):
    class Meta:
        model = Match
        fields = [
            'tournament',
            'match_type',
            'player_1',
            'player_2',
            'judge',
        ]


class CompetitorCreationForm(Form):
    class Meta:
        model = Competitor
        fields = [
            'tournament'
        ]


class FriendCreationFOrm(Form):
    class Meta:
        model = Friend
        field = [
            'name'
        ]


class TrainingCreationForm(Form):
    class Meta:
        model = Training
        fields = [
            'player_1',
            'player_2',
            'match_type',
        ]


class MatchTypeCreationForm(Form):
    class Meta:
        model = MatchType
        fields = [
            'game_type',
            'name',
            'sets',
            'legs',
        ]

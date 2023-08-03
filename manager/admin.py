from django.contrib import admin

from .models import Friend, MatchType, TrainingMatch, Tournament, Competitor, TournamentMatch

admin.site.register(Friend)
admin.site.register(MatchType)
admin.site.register(TrainingMatch)
admin.site.register(Tournament)
admin.site.register(Competitor)
admin.site.register(TournamentMatch)

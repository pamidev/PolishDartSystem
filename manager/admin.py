from django.contrib import admin

from .models import Friend, MatchType, Training, Tournament, Competitor, Match

admin.site.register(Friend)
admin.site.register(MatchType)
admin.site.register(Training)
admin.site.register(Tournament)
admin.site.register(Competitor)
admin.site.register(Match)

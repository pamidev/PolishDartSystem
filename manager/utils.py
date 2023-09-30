from itertools import combinations
from random import shuffle

from .models import Competitor, Match


def create_matches_everybody_with_everybody(tournament):
    competitors = Competitor.objects.filter(tournament=tournament)
    player_combinations = list(combinations(competitors, 2))
    shuffle(player_combinations)

    matches = []
    for player_1, player_2 in player_combinations:
        match = Match.objects.create(
            tournament=tournament,
            player_1=player_1,
            player_2=player_2,
        )
        matches.append(match)

    return matches

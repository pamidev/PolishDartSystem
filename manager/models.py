from django.db import models
from django.db.models import CASCADE
from django.utils import timezone

from accounts.models import CustomUser


class Friend(models.Model):
    buddy_with = models.ForeignKey(CustomUser, blank=False, null=False, on_delete=CASCADE)
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    joined = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    edited = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class MatchType(models.Model):
    GAME_TYPE_CHOICES = [
        ('301', '301'),
        ('501', '501'),
        ('701', '701'),
    ]
    NAME_CHOICES = [
        ('Best of', 'Best of'),
        ('First to', 'First to'),
    ]
    BEST_OF = (
        'Best of',
        (
            ('3', '3'),
            ('5', '5'),
            ('7', '7'),
            ('9', '9'),
            ('11', '11'),
            ('13', '13'),
            ('15', '15'),
            ('17', '17'),
            ('21', '21'),
        ),
    )
    FIRST_TO = (
        'First to',
        (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            ('13', '13'),
            ('14', '14'),
            ('15', '15'),
            ('16', '16'),
            ('17', '17'),
            ('18', '18'),
            ('19', '19'),
            ('20', '20'),
            ('21', '21'),
        ),
    )
    SETS_CHOICES = [
        (
            ('0', 'No sets')
        ),
        FIRST_TO,
        BEST_OF,
    ]
    LEGS_CHOICES = [
        FIRST_TO,
        BEST_OF,
    ]

    game_type = models.CharField(max_length=3, choices=GAME_TYPE_CHOICES, default='501')
    name = models.CharField(max_length=8, choices=NAME_CHOICES, default='First to')
    sets = models.CharField(max_length=2, choices=SETS_CHOICES, default='0')
    legs = models.CharField(max_length=2, choices=LEGS_CHOICES, default='3')

    def __str__(self):
        return f'Game type {self.game_type} - {self.name} {self.sets} sets {self.legs} legs'


class Training(models.Model):
    player_1 = models.OneToOneField(Friend, blank=False, null=False, on_delete=CASCADE, related_name='player_1')
    player_2 = models.OneToOneField(CustomUser, blank=False, null=False, on_delete=CASCADE, related_name='player_2')
    match_type = models.ForeignKey(MatchType, blank=False, null=False, on_delete=CASCADE)
    date_match = models.DateTimeField(auto_now=True)
    player_1_score = models.IntegerField(default=0, verbose_name='player 1 score')
    player_2_score = models.IntegerField(default=0, verbose_name='player 2 score')

    def __str__(self):
        return (f'{self.date_match.date()} - {self.player_1} vs. {self.player_2} '
                f'({self.player_1_score} / {self.player_2_score})')


class Tournament(models.Model):
    name = models.CharField(max_length=128)
    organizer = models.ForeignKey(CustomUser, blank=False, null=False, on_delete=CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=None)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.start_date.date()} - {self.end_date.date()} - {self.name}'


class Competitor(models.Model):
    competitor = models.ForeignKey(CustomUser, blank=False, null=False, on_delete=CASCADE)
    tournament = models.ForeignKey(Tournament, blank=False, null=False, on_delete=CASCADE)
    joined = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, verbose_name='approved')

    def __str__(self):
        return f'{self.competitor}'


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, blank=False, null=False, on_delete=CASCADE)
    match_type = models.ForeignKey(MatchType, blank=False, null=False, on_delete=CASCADE)
    player_1 = models.ForeignKey(Competitor, blank=False, null=False, on_delete=CASCADE, related_name='player_1')
    player_2 = models.ForeignKey(Competitor, blank=False, null=False, on_delete=CASCADE, related_name='player_2')
    judge = models.ForeignKey(Competitor, blank=False, null=False, on_delete=CASCADE, related_name='judge')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=None)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'matches'

    def __str__(self):
        return f'{self.tournament} - {self.player_1} vs. {self.player_2}'

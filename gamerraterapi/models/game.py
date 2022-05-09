from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=55)
    description = models.CharField(max_length=150)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        'Category',
        through='CategoryGame',
        related_name='games'
    )

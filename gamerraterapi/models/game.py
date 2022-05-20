from django.db import models

from gamerraterapi.models.rating import Rating

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
    @property
    # takes method as arguement
    # returns a descriptor object
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        # coming from rating model,
        # filters all rating for each game instance
        ratings = Rating.objects.filter(game=self)
        # Sum all of the ratings for the game
        if len(ratings) == 0:
            # cant return a variable = thing
            average_rating = 0
        else:    
            total_rating = 0
            for rating in ratings:
                total_rating += rating.rating
            average_rating = total_rating/len(ratings)
    
        return average_rating
        #return the result

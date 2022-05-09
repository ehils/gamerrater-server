from django.db import models

class Review(models.Model):
    review = models.CharField(max_length=150)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)

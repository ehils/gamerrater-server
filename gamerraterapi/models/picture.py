from django.db import models

class Picture(models.Model):
    image = models.TextField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
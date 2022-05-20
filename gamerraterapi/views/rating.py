from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from gamerraterapi.models.game import Game
from gamerraterapi.models.player import Player

from gamerraterapi.models.rating import Rating

class RatingView(ViewSet):
    def retrieve(self, request, pk):
        try:
            # player = request.query_params.get('player', None)
            # if player is not None:
            #     ratings = ratings.filter(player_id=player)
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    def list(self, request):
        ratings = Rating.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            ratings = ratings.filter(game_id=game)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rating instance
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk = request.data['game_id'])
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = Rating
        fields = ('id', "rating", "game", "player")
        depth = 2

class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', "rating"]
        
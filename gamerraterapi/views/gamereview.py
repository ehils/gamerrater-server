from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from gamerraterapi.models.game import Game
from gamerraterapi.models.player import Player

from gamerraterapi.models.review import Review

class ReviewView(ViewSet):
    def retrieve(self, request, pk):
        try:
            # player = request.query_params.get('player', None)
            # if player is not None:
            #     Reviews = Reviews.filter(player_id=player)
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    def list(self, request):
        reviews = Review.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            reviews = reviews.filter(game_id=game)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Review instance
        """
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk = request.data['game'])
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Player
        fields = ('user',)
        depth =1
class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    player = PlayerSerializer()
    class Meta:
        model = Review
        fields = ('id', "review", "game", "player")
        depth = 2

class CreateReviewSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(many=False)
    class Meta:
        model = Review
        fields = ['id', "review", "game"]
        

        

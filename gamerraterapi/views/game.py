from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError

from gamerraterapi.models.game import Game
from gamerraterapi.models.player import Player
from gamerraterapi.models.category import Category
from gamerraterapi.views.category import CategorySerializer

class GameView(ViewSet):
    def retrieve(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            # player = request.query_params.get('player', None)
            # if player is not None:
            #     games = games.filter(player_id=player)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        player = Player.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player)
        
        game = Game.objects.get(pk=serializer.data['id'])
        game.categories.add(*request.data['categories'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    categories = CategorySerializer(many=True)
    class Meta:
        model = Game
        fields = ('id', 'description', 'year_released','number_of_players', 'time_to_play', 'age_recommendation', 'player', 'categories')
        depth = 1
class CreateGameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = ['id', 'description', 'year_released','number_of_players', 'time_to_play', 'age_recommendation', 'player']

        

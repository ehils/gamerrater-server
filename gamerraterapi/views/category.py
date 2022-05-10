
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from gamerraterapi.models.category import Category

class CategoryView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        # the following ORM is equivalent to the following SQL execute:
        # db_cursor.execute("""
        #     select id, label
        #     from levelupapi_Category
        #     where id = ?""",(pk,) 
        # )
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Category
        fields = ('id', 'category')
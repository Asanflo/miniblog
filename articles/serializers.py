from rest_framework import serializers

from .models import Articles, Userblog, Category, CommentUser


class UserblogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userblog
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'

    #Fonction permettant de tester les valeurs du champ likes
    def validate_likes(self, like):
        if like is None:
            return 0
        elif like < 0:
            raise serializers.ValidationError("Le nombre de likes ne doit pas etre negatif")
        return like

    def create(self, validated_data):
        if 'likes' not in validated_data or 'likes' is None:
            validated_data['likes'] = 0
        return super().create(validated_data)

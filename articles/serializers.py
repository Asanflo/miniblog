from rest_framework import serializers
from django.contrib.auth.admin import User
from .models import Articles, Userblog, Category, CommentUser



class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    surname = serializers.CharField(source='last_name')
    password = serializers.CharField(write_only=True)
    confirmePassword = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'email', 'password', 'confirmePassword']

    #fonction permettant de valider le mot de passe grace au dictionnaire attrs qui contient les differents champ du serialiser
    def validate(self, attrs):
        if attrs['password'] != attrs['confirmePassword']:
            raise serializers.ValidationError({"password":"Les deux mots de passe ne correspondent pas"})
        return attrs

class UserblogSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = Userblog
        fields = ['user', 'bio', 'avatar']

    #Fonction permettant d'instancier un nouvel utilisateur du blog
    def create(self, validated_data):
        user_content = validated_data.pop('user') #Grace a la methode validated_data, on verifie si le champ user est valide
        user_content.pop('confirmePassword', None)
        user_save = User.objects.create(**user_content) #creation de l'objet user en passant en parametre tout les arguments de user_content
        return Userblog.objects.create(user=user_save, **validated_data)



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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUser
        fields = '__all__'
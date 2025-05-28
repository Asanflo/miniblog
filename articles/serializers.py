from rest_framework import serializers
from django.contrib.auth.admin import User
from .models import Articles, Userblog, Category, CommentUser



class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    surname = serializers.CharField(source='last_name')
    password = serializers.CharField(write_only=True)
    confirmePassword = serializers.CharField(write_only=True)
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'email', 'password', 'confirmePassword']

    #fonction permettant de valider le mot de passe grace au dictionnaire attrs qui contient les differents champ du serialiser

    def validate(self, attrs):
        password = attrs.get('password')
        confirme_password = attrs.get('confirmePassword')
        username = attrs.get('username', None)

        # Récupérer le username si non fourni dans les données mais présent dans l'instance
        if username is None and self.instance:
            username = self.instance.username

        if password or confirme_password:
            if password != confirme_password:
                raise serializers.ValidationError({
                    "password": "Les deux mots de passe ne correspondent pas"
                })

        if username:
            queryset = User.objects.filter(username=username)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({"username": "Ce nom d'utilisateur est déjà utilisé"})

        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('confirmePassword', None)
        print("L'instance est: ", self.instance)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class UserblogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = Userblog
        fields = ['id','user', 'bio', 'avatar']

    #Fonction permettant d'instancier un nouvel utilisateur du blog
    def create(self, validated_data):
        user_content = validated_data.pop('user') #Grace a la methode validated_data, on verifie si le champ user est valide
        user_content.pop('confirmePassword', None)
        user_save = User.objects.create_user(**user_content) #creation de l'objet user en passant en parametre tout les arguments de user_content
        return Userblog.objects.create(user=user_save, **validated_data)


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        # Mise à jour de l’utilisateur lié
        if user_data:
            user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Mise à jour des autres champs
        instance.bio = validated_data.get('bio', instance.bio)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance



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
        if 'likes' not in validated_data or 'likes' == None:
            validated_data['likes'] = 0
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUser
        fields = '__all__'
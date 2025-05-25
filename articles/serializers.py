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

    def validate(self, attrs):
        password = attrs.get('password')
        confirme_password = attrs.get('confirmePassword')

        # Vérifier seulement si un mot de passe est fourni
        if password or confirme_password:
            if password != confirme_password:
                raise serializers.ValidationError({
                    "password": "Les deux mots de passe ne correspondent pas"
                })

        return attrs

    def update(self, instance, validated_data):
        # Supprimer confirmePassword des données validées
        validated_data.pop('confirmePassword', None)

        # Mettre à jour les champs normaux
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Gestion spéciale du mot de passe
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

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

    def update(self, instance, validated_data):
        # Extract user data if present
        user_data = validated_data.pop('user', None)

        # Update Userblog fields (bio, avatar)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update User fields if user_data is provided
        if user_data:
            user_instance = instance.user

            # Handle username uniqueness check
            new_username = user_data.get('username')
            if new_username and new_username != user_instance.username:
                if User.objects.filter(username=new_username).exclude(pk=user_instance.pk).exists():
                    raise serializers.ValidationError({
                        "user": {"username": "Un utilisateur avec ce nom d'utilisateur existe déjà."}
                    })

            # Handle email uniqueness check (if needed)
            new_email = user_data.get('email')
            if new_email and new_email != user_instance.email:
                if User.objects.filter(email=new_email).exclude(pk=user_instance.pk).exists():
                    raise serializers.ValidationError({
                        "user": {"email": "Un utilisateur avec cet email existe déjà."}
                    })

            # Update basic user fields
            user_fields = ['first_name', 'last_name', 'username', 'email']
            for field in user_fields:
                # Map the serializer field names to model field names
                if field == 'first_name' and 'name' in user_data:
                    setattr(user_instance, field, user_data['name'])
                elif field == 'last_name' and 'surname' in user_data:
                    setattr(user_instance, field, user_data['surname'])
                elif field in user_data:
                    setattr(user_instance, field, user_data[field])

            # Handle password update
            password = user_data.get('password')
            if password:
                user_instance.set_password(password)

            user_instance.save()

        instance.save()
        return instance

    def validate(self, attrs):
        # Check password confirmation if both passwords are provided
        user_data = attrs.get('user', {})
        password = user_data.get('password')
        confirm_password = user_data.get('confirmePassword')

        if password and confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError({
                    "user": {"password": "Les deux mots de passe ne correspondent pas."}
                })
        elif password and not confirm_password:
            raise serializers.ValidationError({
                "user": {"confirmePassword": "Veuillez confirmer le mot de passe."}
            })
        elif confirm_password and not password:
            raise serializers.ValidationError({
                "user": {"password": "Le mot de passe est requis."}
            })

        return attrs


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
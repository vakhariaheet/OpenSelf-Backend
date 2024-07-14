from rest_framework import serializers   
from .models import User   

from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
 

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name   
        token['last_name'] = user.last_name
        # Add more custom claims as needed

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password', 'role', "address"]  # Include the fields you want to expose
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):   
        if 'password' in data:
            if len(data['password']) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long")
        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)  # Create a user with the validated data   
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.phone = validated_data.get('phone', instance.phone)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'count', 'arriving_date'] 
        

class UserGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGenre
        fields = ['id', 'user', 'genre']   # Include the fields you want to expose   


class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = ['id', 'user', 'book', 'issue_date', 'return_date']   # Include the fields you want to 'expose
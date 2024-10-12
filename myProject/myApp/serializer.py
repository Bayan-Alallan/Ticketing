from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'email', 'username']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user
    
    #def update(self, instance, validated_data):
        # Update the user's username, email 
     #   instance.username = validated_data.get('username', instance.username)
      #  instance.email = validated_data.get('email', instance.email)

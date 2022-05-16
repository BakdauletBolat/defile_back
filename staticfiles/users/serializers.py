from xml.parsers.expat import model
from rest_framework import serializers
from users.models import CustomUser

class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print(validated_data)
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )

        return user

    class Meta:
        model = CustomUser
        fields = ('id','phone','email','fullname','password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
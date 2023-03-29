from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):

    def create(self, validate_data):
        user = UserModel.objects.create_user(
            username=validate_data['username'],
            password=validate_data['password'],
            email=validate_data['email']
        )
        return user

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email')

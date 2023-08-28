from rest_framework import serializers
from django.contrib.auth import get_user_model
from demo.models import User, UserRole, UserGrChat, GroupChat

UserModel = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):


#     def create(self, validate_data):
#         user = UserModel.objects.create_user(
#             username=validate_data['username'],
#             password=validate_data['password'],
#             email=validate_data['email'],

#         )
#         return user

    def create(self, validate_data):
        user = UserModel.objects.create_user(

        def create(self, validate_data):
            username=validate_data['username'],
            password=validate_data['password'],
#             password=validate_data['password'],
#             email=validate_data['email'],
        )
        user = UserModel.objects.create_user(
            username=validate_data['username'],
            password=validate_data['password'],
#             password=validate_data['password'],
#             email=validate_data['email'],
#         )
        return user


#     class Meta:
#         model = UserModel
#         fields = ('username', 'password', 'email')
#
#
# class MyProfileSerializer(serializers.ModelSerializer):
#     role = serializers.SerializerMethodField()

    def get_role(self, obj):
        return obj.user_role.name

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email', 'age')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        fields = ('old_password', 'new_password')


class GetListUsersSerializers(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        return obj.user_role.name

    class Meta:
        model = UserModel
        fields = ('username', 'title', 'email', 'email_signature', 'tel1', 'tel2', 'role')

    @classmethod
    def setup_eager_loading(cls, queryset):
        pass


class PanigationSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'title', 'email', 'email_signature', 'tel1', 'tel2', 'tel3')


class PostChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGrChat
        fields = ("id", "content_text")


class CreateGroup(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ('id', 'name')


class DeleteGroup(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '_all_'
from rest_framework import serializers
from django.contrib.auth import get_user_model
from demo.models import User, UserRole, UserGrChat, GroupChat

UserModel = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):

    def create(self, validate_data):
        user = UserModel.objects.create_user(

        def create(self, validate_data):
            username=validate_data['username'],
            password=validate_data['password'],
            password=validate_data['password'],
            email=validate_data['email'],
        )
        user = UserModel.objects.create_user(
            username=validate_data['username'],
            password=validate_data['password'],
            password=validate_data['password'],
            email=validate_data['email'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email')


class MyProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        return obj.user_role.name

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email', 'age')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        fields = ('old_password', 'new_password')


class GetListUsersSerializers(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        return obj.user_role.name

    class Meta:
        model = UserModel
        fields = ('username', 'title', 'email', 'email_signature', 'tel1', 'tel2', 'role')

    @classmethod
    def setup_eager_loading(cls, queryset):
        pass


class PanigationSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'title', 'email', 'email_signature', 'tel1', 'tel2', 'tel3')


class PostChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGrChat
        fields = ("id", "content_text")


class CreateGroup(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ('id', 'name')


class DeleteGroup(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = '_all_'

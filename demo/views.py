from django.core.signing import SignatureExpired
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, ListAPIView, get_object_or_404
from rest_framework import permissions, status, generics, pagination, viewsets
from demo.models import User
from demo.serializers import CreateUserSerializers, ChangePasswordSerializer
from demo.serializers import MyProfileSerializer, GetListUsersSerializers, PanigationSerializers
from rest_framework.viewsets import ModelViewSet


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.get_username()
        token['email'] = user.get_email_field_name()

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(CreateAPIView):
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = CreateUserSerializers


class GetProfile(RetrieveUpdateAPIView):
    # permission_classes = [IsAdminUser]
    serializer_class = MyProfileSerializer

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)


class ChangePassword(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request):
        self_object = self.get_object()
        try:
            if self.get_serializer(data=request.data).is_valid():
                if not self_object.check_password(request.data.get("old_password")):
                    return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
                self_object.set_password(request.data.get("new_password"))
                self_object.save()
                response = {
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully'
                }
                return Response(response)
            return Response(self.get_serializer(data=request.data).errors, status=status.HTTP_400_BAD_REQUEST)
        except SignatureExpired:
            return Response(status=status.HTTP_410_GONE)


class GetListUsers(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetListUsersSerializers

    def get_queryset(self):
        queryset = User.objects.filter()

        return queryset

class BillingRecordsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PanigationSerializers
    pagination_class = pagination.PageNumberPagination
    queryset = User.objects.filter().exclude(user_role__name='admin')

    def get_queryset(self):
        user_name = User.objects.get(pk=self.request.user.id)
        if user_name and user_name.user_role.name == 'admin':
            user_name = super().get_queryset()
            return user_name.filter().exclude(user_role__name='admin')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'email': 'demo'})

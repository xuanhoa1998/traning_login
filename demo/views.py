import json

from django.core.signing import SignatureExpired
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    ListCreateAPIView, DestroyAPIView
from rest_framework import permissions, status, generics, pagination, viewsets
from demo.models import User, UserGrChat, GroupChat
from demo.serializers import CreateUserSerializers, ChangePasswordSerializer, PostChatSerializer
from demo.serializers import MyProfileSerializer, GetListUsersSerializers, PanigationSerializers
import requests

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


class GetListUsers(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetListUsersSerializers

    def get_queryset(self):

        # call api GHN
        # url_info = 'https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/detail'
        url_create = 'https://dev-online-gateway.ghn.vn/shiip/public-api/v2/shipping-order/detail'
        headers = {
            "Content-Type": "application/json",
            "Token": "3719c60d-2706-11ee-8bfa-8a2dda8ec551",
            "ShopId": "125248"
        }
        data = {
            "payment_type_id": 2,
            "note": "Tintest 123",
            "required_note": "KHONGCHOXEMHANG",
            "return_phone": "0332190444",
            "return_address": "39 NTT",
            "return_district_id": "null",
            "return_ward_code": "",
            "client_order_code": "1",
            "to_name": "TinTest124",
            "to_phone": "0987654321",
            "to_address": "72 Thành Thái, Phường 14, Quận 10, Hồ Chí Minh, Vietnam",
            "to_ward_code": "20308",
            "to_district_id": 1444,
            "cod_amount": 200000,
            "content": "Theo New York Times",
            "weight": 200,
            "length": 1,
            "width": 19,
            "height": 10,
            "pick_station_id": 1444,
            "deliver_station_id": "null",
            "insurance_value": 10000000,
            "service_id": 0,
            "service_type_id": 2,
            "coupon": "null",
            "pick_shift": [2],
            "items": [
                {
                    "name": "PC gaming",
                    "code": "Polo123",
                    "quantity": 1,
                    "price": 200000,
                    "length": 12,
                    "width": 12,
                    "height": 12,
                    "weight": 1200,
                    "category":
                        {
                            "level1": "Áo"
                        }
                }

            ]
        }
        # end
        response = requests.post(url_create, headers=headers, json=data)
        return response
        # return User.objects.filter().exclude(user_role__name='admin')


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


class PostChat(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostChatSerializer

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id)

    def post(self, request, *args, **kwargs):
        content = request.data.get('content_text')
        id_user = request.user
        group = GroupChat.objects.get(id=request.data.get('group_id'))
        UserGrChat.objects.create(
            content_text=content,
            user_id=id_user,
            group_id=group
        ),
        return Response(status=status.HTTP_200_OK, data={'thanh cong ': 'postChat'})


class CreateGroup(CreateAPIView):
    # def get_queryset(self):
    #     user_name = User.objects.get(pk=self.request.user.id)
    #     return user_name.filter().include(user_role__name='admin')

    def post(self, request, *args, **kwargs):
        name_group = request.data.get('name')

        if request.user.user_role.name == "master":
            GroupChat.objects.create(
                name=name_group
            )
            return Response(status=status.HTTP_200_OK, data={'success': 'success'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'unsuccessful': 'fail'})


class DeleteGroup(DestroyAPIView):

    def delete(self, request, *args, **kwargs):

        # try:
            gr_id = request.data.get("gr_user_id")
            group_delete = GroupChat.objects.get(pk=gr_id)
            if group_delete:
                group_delete.delete()
                return Response(status=status.HTTP_200_OK, data={'delete success'})

        # Exception

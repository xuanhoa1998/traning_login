from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView 

from demo.views import MyTokenObtainPairView, CreateUserView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('createuser/', CreateUserView.as_view() )
]

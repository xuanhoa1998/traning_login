from django.urls import path
from demo.views import MyTokenObtainPairView, CreateUserView, GetProfile, ChangePassword

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('createuser/', CreateUserView.as_view(), name='createUserViews'),
    path('getprofile/', GetProfile.as_view(), name='GetProfile'),
    path('changePassword/', ChangePassword.as_view(), name='GetProfile')
]

from django.urls import path
from demo.views import MyTokenObtainPairView, CreateUserView,\
        GetProfile, ChangePassword, GetListUsers, BillingRecordsView, PostChat, CreateGroup, DeleteGroup, GetListUserInOneGroupView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('createuser/', CreateUserView.as_view(), name='createUserViews'),
    path('getprofile/', GetProfile.as_view(), name='GetProfile'),
    path('changePassword/', ChangePassword.as_view(), name='GetProfile'),
    path('getListUsers/', GetListUsers.as_view(), name='getListUsers'),
    path('getPanigations/', BillingRecordsView.as_view(), name='GetPanigation'),
    path('postChat/', PostChat.as_view(), name='postChat'),
    path('createGroup/', CreateGroup.as_view(), name='createGroup'),
    path('deleteGroup/', DeleteGroup.as_view(), name='deleteGroup'),
    path('getListUserInOneGr/<str:pk>', GetListUserInOneGroupView.as_view(), name='GetListUserInOneGroupView'),


]

from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("demo.url")),
    path(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]

"""
URL configuration for vault project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.verify_view import VerifyViewSet
from users.profile_views import ProfileViewSet
from users.user_views import UserViewSet
from users.auth_views import AuthViewSet
from file.files_views import FilesViewSet
from file.file_share_views import FileShareViewSet
from file.file_share_link_views import FileShareLinkViewSet

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profiles")
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"verify", VerifyViewSet, basename="verify")
router.register(r"files/share/link", FileShareLinkViewSet, basename="files_share_link")
router.register(r"files/share", FileShareViewSet, basename="files_share")
router.register(r"files", FilesViewSet, basename="files")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/<uuid:pk>/profile", UserViewSet.as_view({"get": "profile"})),
    path("users/<uuid:pk>/", UserViewSet.as_view({"get": "user_by_id"})),
    path("users/", UserViewSet.as_view({"post": "create_user", "get": "user_list"})),
    path("users/me", UserViewSet.as_view({"get": "me"})),
    path("", include(router.urls)),
]

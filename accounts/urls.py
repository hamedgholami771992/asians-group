from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views.user import UserViewSet

user_list = UserViewSet.as_view({
    "get": "list",
    "post": "create",
})
user_detail = UserViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

urlpatterns = [
    # Registration & listing
    path("", user_list, name="user-list-create"),   # GET=list, POST=create
    path("<int:pk>/", user_detail, name="user-detail"),  # GET/PUT/PATCH/DELETE user

    # JWT
    path("login/", TokenObtainPairView.as_view(), name="user-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # Custom actions
    path("me/", UserViewSet.as_view({"get": "me", "put": "me", "patch": "me"}), name="user-me"),
    path("<int:pk>/promote/", UserViewSet.as_view({"post": "promote"}), name="user-promote"),
]
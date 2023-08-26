from django.urls import path

# from .views import view의 함수명
from .views import (
    register,
    login,
    logout,
    userpage,
    search,
    delete,
    reading,
    wish,
    usercommunity,
)

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("logout/", logout),
    path("userpage/<str:pk>/", userpage),
    path("search/", search),
    path("delete/", delete),
    path("userpage/<str:pk>/reading/", reading),
    path("userpage/<str:pk>/wish/", wish),
    path("userpage/<str:pk>/usercommunity/", usercommunity),
]

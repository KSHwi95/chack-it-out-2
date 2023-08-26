from django.urls import path
from .views import search, result, result2
from user.views import userpage

urlpatterns = [
    path("search/", search),
    path("search/result/<str:pk>/", result),
    path("search/result2/<str:pk>/", result2),
    path("userpage/<str:pk>/", userpage),
]

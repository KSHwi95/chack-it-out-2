from django.urls import path
from .views import community, newcommunity,detail,quit,detail2

urlpatterns = [path("", community), 
              path("new/", newcommunity),
              path("detail/<str:pk>", detail),
              path("detail2/<str:pk>", detail2),
              path("quit/<str:pk>",quit)            
              ]

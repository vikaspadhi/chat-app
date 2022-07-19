from django.urls import path
from .views import home  , channels

urlpatterns = [
    # path('',home),
    path('<str:group_name>/',channels),
]



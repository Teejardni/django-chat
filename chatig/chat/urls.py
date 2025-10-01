from django.urls import path
from .views import room
urlpatterns = [ path("chat/<str:room_name>/", room, name="room"), ]

from django.shortcuts import render
from .models import Message

def room(request, room_name):
    history = Message.objects.filter(room=room_name).order_by("timestamp")[:100]
    return render(request, "chat/room.html", {"room_name": room_name, "history": history})



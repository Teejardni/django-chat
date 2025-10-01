import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data or "{}")
        text = (payload.get("text") or "").strip()
        if not text:
            return
        user = self.scope.get("user", AnonymousUser())
        msg = await self._save_message(user, text)
        data = {
            "user": (user.username if user and user.is_authenticated else "anon"),
            "text": msg.text,
            "timestamp": msg.timestamp.isoformat(),
            "room": msg.room,
        }
        await self.channel_layer.group_send(self.group_name, {"type": "chat.message", "data": data})

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    @database_sync_to_async
    def _save_message(self, user, text):
        user_obj = user if getattr(user, "is_authenticated", False) else None
        return Message.objects.create(room=self.room_name, user=user_obj, text=text)

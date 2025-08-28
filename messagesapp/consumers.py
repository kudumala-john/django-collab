import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message
from tasksapp.models import Project

class ProjectChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope["url_route"]["kwargs"]["project_id"]
        self.group = f"project_{self.project_id}"
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            await self.close()
            return
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = (data.get("message") or "").strip()
        if not msg:
            return
        user = self.scope["user"]
        saved = await self._save(user, msg)
        payload = {
            "message": saved.content,
            "user": user.username,
            "timestamp": saved.created_at.strftime("%H:%M"),
        }
        await self.channel_layer.group_send(self.group, {"type": "chat.message", "payload": payload})

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["payload"]))

    @sync_to_async
    def _save(self, user, content):
        project = Project.objects.get(pk=self.project_id)
        return Message.objects.create(project=project, user=user, content=content)

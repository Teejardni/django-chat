from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    room = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]


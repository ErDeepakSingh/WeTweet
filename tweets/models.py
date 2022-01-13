from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL



class Tweet(models.Model):
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets") # many users can many tweets

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-id']

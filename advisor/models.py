from django.db import models

from accounts.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
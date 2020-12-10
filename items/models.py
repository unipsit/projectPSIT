from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Item(models.Model):
    item_name = models.CharField(max_length=10, unique=True)
    where = models.CharField(max_length=100, default='')
    need_at = models.DateTimeField(default=timezone.now)
    post_at = models.DateTimeField(auto_now_add=True)
    post_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name

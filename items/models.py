from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Item(models.Model):
    item_name = models.CharField(max_length=10)
    pic_item = models.ImageField(default='item_default.jpg', upload_to='item_pics')
    where = models.CharField(max_length=100, default='')
    need_at = models.DateTimeField(default=timezone.now)
    post_at = models.DateTimeField(auto_now_add=True)
    post_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    accept_by = models.ForeignKey(User, related_name='accepts', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Yet')
    return_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})

class Icon(models.Model):
    trash = models.ImageField(default='trash_icon.png')
    true_rec = models.ImageField(default='true_icon.png')
    cant = models.ImageField(default='false_icon.png')
    edit = models.ImageField(default='edit_icon.png')

from django.db import models
from ranobe.models import Ranobe
from django.contrib.auth.models import User


class Comments(models.Model):
    ranobe = models.ForeignKey(Ranobe, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, )
    text = models.TextField(max_length=600, default=" ")

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.text

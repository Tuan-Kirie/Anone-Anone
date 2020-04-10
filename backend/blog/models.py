from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} опубликован {self.published_date} автор {self.name}"

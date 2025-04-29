from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Experience(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    image = models.ImageField(upload_to='experiences/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='experiences')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
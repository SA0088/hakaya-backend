from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    photo =models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Experience(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    image_path = models.ImageField(upload_to='experiences/', default='default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='experiences')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    liked_by = models.ManyToManyField(User, related_name='liked_experiences', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.liked_by.count()

    def toggle_like(self, user):
        if user in self.liked_by.all():
            self.liked_by.remove(user)
            return "Like removed", self.likes_count
        else:
            self.liked_by.add(user)
            return "Experience liked", self.likes_count

class Review(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    liked_by = models.ManyToManyField(User, related_name="liked_reviews", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.experience.title} by {self.user.username}'

    @property
    def likes_count(self):
        return self.liked_by.count()

    def toggle_like(self, user):
        if user in self.liked_by.all():
            self.liked_by.remove(user)
            return "Like removed", self.likes_count
        else:
            self.liked_by.add(user)
            return "Review liked", self.likes_count

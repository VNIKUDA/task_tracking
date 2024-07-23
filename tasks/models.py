from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Task(models.Model):

    STATUS_CHOICES = (
        ("todo", "Назначено"),
        ("in_progress", "В процесі"),
        ("done", "Виконано")
    )

    PRIORITY_CHOICES = (
        ("low", "Низький"),
        ("medium", "Середній"),
        ("high", "Високий")
    )

    title = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("tasks:task-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ["-due_date", "-created"]

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    media = models.FileField(upload_to="comments_media/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return self.task.get_absolute_url()
    
    def get_media_name(self):
        return self.media.name.split("/")[-1]

    def delete(self, *args, **kwargs):
        self.media.delete()
        super(Comment, self).delete(*args, **kwargs)
    
    class Meta:
        ordering = ["-created_at"]
    
class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}"
    
    class Meta:
        unique_together = ("comment", "author")
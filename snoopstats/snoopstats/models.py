from django.db import models

class Post(models.Model):
    # Platform-specific fields
    PLATFORM_CHOICES = [
        ('google', 'Google'),
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
    ]
    
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    title = models.CharField(max_length=255)
    views = models.IntegerField()
    likes = models.IntegerField()
    shares = models.IntegerField()
    comments = models.IntegerField()

    def __str__(self):
        return self.title

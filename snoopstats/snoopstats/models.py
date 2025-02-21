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

### _______________________WEBsiteInfo_________
class WebsiteInfo(models.Model):
    
    SECTION_CHOICES = [
        ('about', 'About'),
        ('contact', 'Contact'),
        ('services', 'Services'),
    ]

    section = models.CharField(max_length=20, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()  # Content for each section

    def __str__(self):
        return self.title




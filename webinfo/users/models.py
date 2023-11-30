from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_users'  
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users'  
    )
    
 
    username = models.CharField(
        max_length=150,
        unique=True,
    )

    email = models.EmailField()
    otp = models.CharField(max_length=6, null=True, blank=True)
    password = models.CharField(max_length=128)  
    user_type = models.CharField(max_length=20)
    USER_TYPE_CHOICES = (
        ('researcher', 'Researcher'),
        ('health_official', 'Health Official'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class DownloadDataModel(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.name
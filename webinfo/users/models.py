from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_users'  # Custom related name for groups
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users'  # Custom related name for user_permissions
    )
    
 
    username = models.CharField(
        max_length=150,
        unique=True,
    )

    email = models.EmailField()
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

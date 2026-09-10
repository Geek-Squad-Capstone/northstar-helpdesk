from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    role_options = [
        ("employee", "Employee"),
        ("technician", "IT Technician"),
        ("administrator", "IT Administrator"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=role_options,
        default="employee"
    )

    def __str__(self):
        return self.user.username

# Create your models here


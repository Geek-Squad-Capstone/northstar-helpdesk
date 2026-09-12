from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    role_options = [
        ("regular_user", "Regular User"),
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
        default="regular_user"
    )

    def __str__(self):
        return self.user.username

# Create your models here
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_status = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

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

class Ticket(models.Model):

    submitted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="submitted_tickets"
    )

    assigned_technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="category_tickets"
    )

    title = models.CharField(max_length=200)

    affected_device_system = models.CharField(max_length=200)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        default="Open"
    )

    priority = models.CharField(max_length=20)

    department = models.CharField(max_length=100)

    created_date = models.DateTimeField(auto_now_add=True)

    last_updated_date = models.DateTimeField(auto_now=True)

    resolved_date = models.DateTimeField(
        null=True,
        blank=True
    )

    closed_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

class Comment(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    comment_text = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
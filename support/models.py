from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


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

    device_choices = [
        ("Desktop", "Desktop"),
        ("Laptop", "Laptop"),
        ("Mobile Device", "Mobile Device"),
        ("Printer", "Printer"),
        ("Network", "Network"),
        ("Software/Application", "Software/Application"),
        ("Other", "Other"),
    ]

    priority_choices = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    department_choices = [
        ("IT", "IT"),
        ("Human Resources", "Human Resources"),
        ("Finance", "Finance"),
        ("Operations", "Operations"),
    ]

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

    affected_device_system = models.CharField(
        max_length=200,
        choices = device_choices
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        default="Open"
    )

    priority = models.CharField(
        max_length=20,
        choices = priority_choices
    )

    department = models.CharField(
        max_length=100,
        choices = department_choices
    )

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

    @property
    def long_unassigned(self):
        if self.assigned_technician is None and (timezone.now() - self.created_date) >= timedelta(hours=24):
            return True
        return False

    def change_status(self,user, new_status):
        old_status = self.status
        self.status = new_status
        self.save()

        AuditLog.objects.create(
            user=user,
            ticket=self,
            action=f"Status changed from {old_status} to {new_status}"
	)

    def assign_ticket(self, user, technician):
        self.assigned_technician = technician
        self.save()
	
        AuditLog.objects.create(
            user=user,
            ticket=self,
            action=f"Ticket assigned to {technician.username}"
        )

    def close_ticket(self, user):
        self.status = "Closed"
        self.save()

        AuditLog.objects.create(
            user=user,  
            ticket=self,
            action=f"Ticket closed"
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

class AuditLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="audit_logs"
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.PROTECT,
        related_name="audit_logs"
    )

    action = models.CharField(max_length=100)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"

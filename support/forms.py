from django import forms
from .models import Ticket, Category, Comment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "category",
            "title",
            "affected_device_system",
            "description",
            "priority",
            "department",
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
from django import forms
from .models import Ticket, Category, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class AdminUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserProfile.role_options
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "role"]

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data["role"]
            )

        return user
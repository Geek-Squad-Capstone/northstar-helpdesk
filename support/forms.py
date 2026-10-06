from django import forms
from .models import Ticket

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

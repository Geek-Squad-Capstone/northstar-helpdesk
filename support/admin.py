from django.contrib import admin
from .models import Ticket


# Register your models here.

from django.contrib import admin
from .models import UserProfile, Ticket

admin.site.register(UserProfile)
admin.site.register(Ticket)

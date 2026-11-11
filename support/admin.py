from django.contrib import admin
from .models import Category, Ticket, UserProfile

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Ticket)

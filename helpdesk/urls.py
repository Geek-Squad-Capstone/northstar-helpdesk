"""
URL configuration for helpdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from support import views

urlpatterns = [
    path(
        'admin/', 
        admin.site.urls
        ),
    
    path(
        '', 
        views.index, 
        name='home'
        ),
    
    path(
        'dashboard/', 
        views.dashboard, 
        name='dashboard'
        ),
    
    path(
        'tickets/', 
        views.tickets, 
        name='tickets'
        ),
    
    path(
        'tickets/create/', 
        views.create_ticket, 
        name='create_ticket'
        ),
    
    path(
        'tickets/<int:ticket_id>/assign/', 
        views.assign_technician, 
        name='assign_technician'
        ), 
    
    path(
        'accounts/', 
        include('django.contrib.auth.urls')
        ),
    
    path(
        "ticket/queue/",
        views.ticket_queue,
        name="ticket_queue"
        ),
    
    path(
        "categories/",
        views.category_management,
        name="category_management"
        ),
    
    path(
        "categories/<int:category_id>/toggle/",
        views.toggle_category_status,
        name="toggle_category_status"
        ),
    
    path(
        "tickets/<int:ticket_id>/claim/",
        views.claim_ticket,
        name="claim_ticket"
        ),
    
    path(
        "ticket/<int:ticket_id>/edit-status/",
        views.edit_ticket_status,
        name="edit_ticket_status",
        ),
    
    path(
        "ticket/<int:ticket_id>/ticket_detail/",
        views.ticket_detail,
        name="ticket_detail"
        ),
    
    path(
        "ticket/<int:ticket_id>/edit-priority/", 
        views.edit_ticket_priority, 
        name="edit_ticket_priority"
        ),
    
    path(
        "ticket/<int:ticket_id>/edit-category/", 
        views.edit_ticket_category, 
        name="edit_ticket_category"
        ),

    path(
        "ticket/<int:ticket_id>/add-internal-note/",
        views.add_internal_note,
        name="add_internal_note"
    ),

    path(
        "ticket/<int:ticket_id>/reopen_ticket/",
        views.reopen_ticket,
        name="reopen_ticket"
    ),
]

from django.contrib import admin
from django.urls import include, path
from support import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:ticket_id>/assign/', views.assign_technician, name='assign_technician'),
    path('ticket/queue/', views.ticket_queue, name='ticket_queue'),
    path('categories/', views.category_management, name='category_management'),
    path('categories/<int:category_id>/toggle/', views.toggle_category_status, name='toggle_category_status'),
]
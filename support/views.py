from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .permissions import role_required

#  Create your views here.
def index(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@role_required("regular_user")
def tickets(request):
    tickets = Ticket.objects.filter(submitted_by=request.user).order_by("-created_date")

    return render(request, 'tickets.html', {'tickets': tickets})
    
@role_required("technician", "administrator")
def ticket_queue(request):
    tickets = Ticket.objects.exclude(
        status="Closed"
    ).order_by("-created_date")

    return render(
        request,
        "ticket_queue.html",
        {"tickets": tickets}
    )

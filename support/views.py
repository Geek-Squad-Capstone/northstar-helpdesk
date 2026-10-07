from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .permissions import role_required
from .forms import TicketForm
from django.contrib import messages

#  Create your views here.
def index(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.submitted_by = request.user
            ticket.save()

        messages.success(
            request,
            "Your ticket has been submitted successfully."
        )
        
        return redirect("dashboard")

    else:
        form = TicketForm()

    return render(request, "create_ticket.html", {"form": form})

@role_required("regular_user")
def tickets(request):
    tickets = Ticket.objects.filter(submitted_by=request.user).order_by("-created_date")

    return render(request, 'tickets.html', {'tickets': tickets})
    

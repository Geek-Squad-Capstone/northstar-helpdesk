from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, UserProfile, Category
from .permissions import role_required
from .forms import TicketForm, CategoryForm
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

@role_required("administrator")
def category_management(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("category_management")
    else:
        form = CategoryForm()

    categories = Category.objects.all().order_by("category_name")

    return render(
        request,
        "category_management.html",
        {
            "form": form,
            "categories": categories,
        }
    )


@role_required("administrator")
def toggle_category_status(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.category_status = not category.category_status
        category.save()

    return redirect("category_management")
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from .models import Ticket, UserProfile, Category
from .permissions import role_required
from .forms import TicketForm, CategoryForm


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
    tickets = Ticket.objects.filter(
        submitted_by=request.user
    ).order_by("-created_date")

    return render(request, 'tickets.html', {'tickets': tickets})


@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
def assign_technician(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    current_user_profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if current_user_profile.role != 'administrator':
        return HttpResponseForbidden(
            "You do not have permission to assign technicians."
        )

    if request.method == 'POST':
        technician_id = request.POST.get('technician')

        if technician_id:
            technician = get_object_or_404(
                UserProfile,
                user_id=technician_id,
                role='technician'
            )
            ticket.assigned_technician = technician.user
            ticket.save()

        return redirect('ticket_list')

    technicians = UserProfile.objects.filter(
        role='technician'
    ).select_related('user')

    return render(
        request,
        'tickets/assign_technician.html',
        {
            'ticket': ticket,
            'technicians': technicians,
        }
    )


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
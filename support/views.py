from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, UserProfile, Category, InternalNote, User 
from .permissions import PermissionDenied, role_required
from .forms import TicketForm, CategoryForm, CommentForm, AdminUserCreationForm
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

@role_required("regular_user", "administrator")
def tickets(request):
    tickets = Ticket.objects.filter(submitted_by=request.user).order_by("-created_date")

    return render(request, 'tickets.html', {'tickets': tickets})
    
@role_required("technician", "administrator")
def ticket_queue(request):
    tickets = Ticket.objects.exclude(
        status="Closed"
    ).order_by("-created_date")

    status = request.GET.get("status")
    if status:
        tickets = tickets.filter(status=status)

    department = request.GET.get("department")
    if department:
        tickets = tickets.filter(department=department)

    category = request.GET.get("category")
    if category:
        tickets = tickets.filter(category_id=category)

    assignment = request.GET.get("assignment")
    if assignment == "unassigned":
        tickets = tickets.filter(assigned_technician__isnull=True)
    elif assignment == "assigned":
        tickets = tickets.filter(assigned_technician__isnull=False)

    submitted_by = request.GET.get("submitted_by")
    if submitted_by:
        tickets = tickets.filter(submitted_by_id=submitted_by)

    ticket_number = request.GET.get("ticket_number")
    if ticket_number:
        tickets = tickets.filter(id=ticket_number)

    assigned_technician = request.GET.get("assigned_technician")
    if assigned_technician:
        tickets = tickets.filter(assigned_technician_id=assigned_technician)

    departments = Ticket.department_choices
    categories = Category.objects.all().order_by("category_name")
    submitters = User.objects.all().order_by("username")
    technicians = User.objects.filter(
        profile__role="technician"
    ).order_by("username")

    return render(
        request,
        "ticket_queue.html",
        {
            "tickets": tickets,
            "departments": departments,
            "categories": categories,
            "submitters": submitters,
            "technicians": technicians
        }
    )

@role_required("technician", "administrator")
def closed_ticket_history(request):
    tickets = Ticket.objects.filter(
        status="Closed"
    ).order_by("-closed_date")

    department = request.GET.get("department")
    if department:
        tickets = tickets.filter(department=department)

    category = request.GET.get("category")
    if category:
        tickets = tickets.filter(category_id=category)

    assignment = request.GET.get("assignment")
    if assignment == "unassigned":
        tickets = tickets.filter(assigned_technician__isnull=True)
    elif assignment == "assigned":
        tickets = tickets.filter(assigned_technician__isnull=False)

    submitted_by = request.GET.get("submitted_by")
    if submitted_by:
        tickets = tickets.filter(submitted_by_id=submitted_by)

    ticket_number = request.GET.get("ticket_number")
    if ticket_number:
        tickets = tickets.filter(id=ticket_number)

    assigned_technician = request.GET.get("assigned_technician")
    if assigned_technician:
        tickets = tickets.filter(assigned_technician_id=assigned_technician)

    departments = Ticket.department_choices
    categories = Category.objects.all().order_by("category_name")
    submitters = User.objects.all().order_by("username")
    technicians = User.objects.filter(
        profile__role="technician"
    ).order_by("username")

    return render(
        request,
        "closed_ticket_history.html",
        {
            "tickets": tickets,
            "departments": departments,
            "categories": categories,
            "submitters": submitters,
            "technicians": technicians
        }
    )

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if (request.user != ticket.submitted_by and request.user.profile.role not in ["technician", "administrator"]
    ):
        raise PermissionDenied

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect("ticket_detail", ticket_id=ticket.id)
    else:
        comment_form = CommentForm()
    
    return render(
        request,
        "ticket_detail.html",
        {"ticket": ticket,
         "comment_form": comment_form}
    )

@role_required("technician", "administrator")
def edit_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    status_choices = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed",
    ]

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in status_choices:
            ticket.change_status(request.user, new_status)
            return redirect("ticket_queue")

    return render(
        request,
        "edit_ticket_status.html",
        {
            "ticket": ticket,
            "status_choices": status_choices,
        }
    )

@role_required("technician")
def claim_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method != "POST":
        return redirect("ticket_queue")

    if ticket.assigned_technician is not None:
        messages.error(
            request,
            "This ticket has already been assigned."
        )
        return redirect("ticket_queue")

    ticket.assign_ticket(
        user=request.user,
        technician=request.user
    )

    messages.success(
        request,
        f"Ticket {ticket.id} has been assigned to you."
    )

    return redirect("ticket_queue")

@role_required("administrator")
def assign_technician(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        technician_id = request.POST.get("technician")

        technician = get_object_or_404(
            UserProfile,
            user_id=technician_id,
            role="technician"
        )

        ticket.assigned_technician = technician.user
        ticket.save()

        messages.success(
            request,
            f"Ticket {ticket.id} has been assigned to {technician.user.username}."
        )

        return redirect("ticket_queue")

    technicians = UserProfile.objects.filter(
        role="technician"
    ).select_related("user")

    return render(
        request,
        "tickets/assign_technician.html",
        {
            "ticket": ticket,
            "technicians": technicians,
        }
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

@role_required("technician")
def edit_ticket_priority(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    priority_choices = [choice[0] for choice in Ticket.priority_choices]

    if request.method == "POST":
        new_priority = request.POST.get("priority")

        if new_priority in priority_choices:
            ticket.priority = new_priority
            ticket.save()
            return redirect("ticket_queue")

    return render(
        request,
        "edit_ticket_priority.html",
        {
            "ticket": ticket,
            "priority_choices": priority_choices,
        }
    )

@role_required("technician")
def edit_ticket_category(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    active_categories = Category.objects.filter(category_status=True)

    if request.method == "POST":
        category_id = request.POST.get("category")

        selected_category = active_categories.filter(id=category_id).first()

        if selected_category:
            ticket.category = selected_category
            ticket.save()
            return redirect("ticket_queue")

    return render(
        request,
        "edit_ticket_category.html",
        {
            "ticket": ticket,
            "active_categories": active_categories,
        }
    )

@role_required("technician")
def add_internal_note(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        note_text = request.POST.get("note_text", "").strip()

        if note_text:
            InternalNote.objects.create(
                ticket=ticket,
                author=request.user,
                note_text=note_text
            )

    return redirect("ticket_detail", ticket_id=ticket.id)

@role_required("regular_user")
def reopen_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user != ticket.submitted_by:
        raise PermissionDenied

    if request.method == "POST" and ticket.status == "Closed":
        ticket.reopen_ticket(request.user)

    return redirect(
        "ticket_detail",
        ticket_id=ticket.id
    )

@role_required("administrator")
def user_management(request):
    if request.method == "POST":
        form = AdminUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("user_management")
    else:
        form = AdminUserCreationForm()

    users = User.objects.select_related("profile").order_by("username")

    return render(
        request,
        "user_management.html",
        {
            "form": form,
            "users": users,
            "role_options": UserProfile.role_options
        }
    )

@role_required("administrator")
def change_user_role(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        raise PermissionDenied

    if request.method == "POST":
        role = request.POST.get("role")

        valid_roles = [value for value, label in UserProfile.role_options]

        if role in valid_roles:
            target_user.profile.role = role
            target_user.profile.save()
    
    return redirect("user_management")

@role_required("administrator")
def deactivate_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        raise PermissionDenied

    if request.method == "POST":
        target_user.is_active = False
        target_user.save()

    return redirect("user_management")
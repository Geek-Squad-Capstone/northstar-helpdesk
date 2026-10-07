from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Ticket, UserProfile


def index(request):
    return render(request, 'home.html')


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
        return HttpResponseForbidden("You do not have permission to assign technicians.")

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
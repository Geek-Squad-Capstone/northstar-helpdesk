from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#  Create your views here.
def index(request):
    return render(request, 'home.html')
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
@login_required
def tickets(request):
    return render(request, 'tickets.html')

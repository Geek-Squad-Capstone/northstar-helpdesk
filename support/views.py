from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def tickets(request):
    return render(request, 'tickets.html')

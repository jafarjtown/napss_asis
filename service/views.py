from django.shortcuts import render, redirect
from .models import ServiceType, ServicePriority, Service, StudentService
from django.contrib import messages
# Create your views here.

def services(request):
  services = Service.objects.all()
  return render(request, 'service/index.html', { 'services': services})

def add_service(request):
  priorities = ServicePriority.objects.all()
  services = ServiceType.objects.all()
  
  if request.method == 'POST':
    service_type = request.POST.get('service')
    service_priority = request.POST.get('priority')
    service_information = request.POST.get('information')
    s_type = ServiceType.objects.get(id=service_type)
    s_priority = ServicePriority.objects.get(id=service_priority)
    user_wallet = request.user.wallet 
    total_expense = s_type.price * s_priority.level
    if user_wallet.amount < total_expense:
      messages.error(request, 'Insufficient balance for the service')
    else:
      messages.success(request, 'Service booked successful.')
      service = Service.objects.create(type=s_type, priority=s_priority, information=service_information, price=total_expense)
      user_wallet.balance -= total_expense
      user_wallet.save()
  return render(request, 'service/add.html', {'services':services, 'priorities':priorities})

def service_details(request, service_id):
  service = Service.objects.get(id=service_id)
  return render(request, 'service/details.html', {'service':service})

def cancel_service(request, service_id):
  return redirect('service:details', service_id)

def complete_service(request, service_id):
  return render(request, 'service/details.html')
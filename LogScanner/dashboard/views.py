from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required 
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {})

def app_logs_view(request):

    return render(request, 'dashboard/app_logs.html', {'is_analysis_page': True})

#  Authentication Logs
def auth_logs_view(request):

    return render(request, 'dashboard/auth_logs.html', {'is_analysis_page': True})

#  Network Logs
def network_logs_view(request):

    return render(request, 'dashboard/network_logs.html', {'is_analysis_page': True})
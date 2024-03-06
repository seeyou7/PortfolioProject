from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#analyzing part
from .log_analysis.application import analyze_application_logs
from .log_analysis.auth import analyze_auth_logs
from .log_analysis.network import analyze_network_logs
from django.conf import settings
import os # this to check the path with the print error
import logging
# pour un afichage sur plusieur line de json output
from os import path
import json


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {})

@login_required
def app_logs_view(request):
    log_file_path = settings.LOG_FILE_PATHS.get('application')  # Make sure 'application' is correctly defined in settings.LOG_FILE_PATHS
    analysis_results = {}  # Initialize to ensure it's always a dict for consistency

    try:
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                log_content = file.read()
                # Assume analyze_application_logs returns a dictionary
                analysis_results = analyze_application_logs(log_content)
                # Check if analysis_results is a dictionary and format it
                if isinstance(analysis_results, dict):
                    analysis_results = json.dumps(analysis_results, indent=4)
        else:
            analysis_results = "Application log file not found."
    except Exception as e:
        # Catch any exception and return a simple error message
        analysis_results = f"An error occurred: {str(e)}"

    context = {
        'is_analysis_page': True,
        'analysis_results': analysis_results,  # Pass the formatted JSON string to the template
    }
    return render(request, 'dashboard/app_logs.html', context)

@login_required # afficher les res en format json en claire
def auth_logs_view(request):
    log_file_path = settings.LOG_FILE_PATHS.get('auth')
    analysis_results = {}  # Initialize to ensure it's always a dict for consistency

    try:
        if path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                log_content = file.read()
                # Assume analyze_auth_logs returns a dictionary
                analysis_results = analyze_auth_logs(log_content)
                # Check if analysis_results is a dictionary and format it
                if isinstance(analysis_results, dict):
                    analysis_results = json.dumps(analysis_results, indent=4)
        else:
            analysis_results = "Auth log file not found."
    except Exception as e:
        # Catch any exception and return a simple error message
        analysis_results = f"An error occurred: {str(e)}"

    context = {
        'is_analysis_page': True,
        'analysis_results': analysis_results, 
    }
    
    return render(request, 'dashboard/auth_logs.html', context)

#  Network Logs
@login_required
def network_logs_view(request):
    analysis_results = analyze_network_logs()
    return render(request, 'dashboard/network_logs.html', {'is_analysis_page': True,  'analysis_results': analysis_results})

# Set up logging
# logger = logging.getLogger(__name__)

# @login_required
# def auth_logs_view(request):
#     log_file_path = settings.LOG_FILE_PATHS.get('auth')
#     analysis_results = {}  # Initialize as a dictionary

#     try:
#         if os.path.exists(log_file_path):
#             with open(log_file_path, 'r') as file:
#                 log_content = file.read()
#                 analysis_results = analyze_auth_logs(log_content)
#         else:
#             # Log file not found error
#             logger.error(f"Auth log file not found at path: {log_file_path}")
#             analysis_results['error'] = "Auth log file not found."
#     except Exception as e:
#         # Log the exception details
#         logger.exception("An error occurred while analyzing auth logs:")
#         # Provide a generic error message for the user, while logging specific details
#         analysis_results['error'] = "An unexpected error occurred while processing the logs. Please try again later."
    
#     return render(request, 'dashboard/auth_logs.html', {
#         'is_analysis_page': True,
#         'analysis_results': analysis_results,
#     })
  # Ensure this import matches the location of your function
# @login_required
# def auth_logs_view(request):
#     log_file_path = settings.LOG_FILE_PATHS.get('auth')
#     analysis_results = {}  # Initialize as a dictionary

#     try:
#         if os.path.exists(log_file_path):
#             with open(log_file_path, 'r') as file:
#                 log_content = file.read()
#                 analysis_results = analyze_auth_logs(log_content)
#         else:
#             # Even if the file is not found, set a meaningful message within the dictionary
#             analysis_results['error'] = "Auth log file not found."
#     except Exception as e:
#         # Catch any other exceptions and store the message within the dictionary
#         analysis_results['error'] = str(e)
    
#     return render(request, 'dashboard/auth_logs.html', {
#         'is_analysis_page': True,
#         'analysis_results': analysis_results,
#     })

# def app_logs_view(request):
#     analysis_results = analyze_application_logs()
#     return render(request, 'dashboard/app_logs.html', {'is_analysis_page': True, 'analysis_results': analysis_results})

# @login_required
# def auth_logs_view(request):
#     log_file_path = settings.LOG_FILE_PATHS.get('auth')
    
#     if os.path.exists(log_file_path):
#         try:
#             with open(log_file_path, 'r') as file:
#                 log_content = file.read()
#                 analysis_results = analyze_auth_logs(log_content)
#         except Exception as e:
#             analysis_results = str(e)
#     else:
#         analysis_results = "auth log file not found."
    
#     return render(request, 'dashboard/auth_logs.html', {
#         'is_analysis_page': True,
#         'analysis_results': analysis_results,
#     })
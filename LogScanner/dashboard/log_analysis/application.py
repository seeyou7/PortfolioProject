# log_analysis/application.py
from django.conf import settings
# from django.http import HttpResponse
# def test_log_path(request):
#     app_log_path = settings.LOG_FILE_PATHS.get('application')
#     # Print the path to the console
#     print(app_log_path)
#     # Also return it as an HTTP response for testing
#     return HttpResponse(f"Application Log Path: {app_log_path}")

def analyze_application_logs():
    log_file_path = settings.LOG_FILE_PATHS.get('application')
    try:
        with open(log_file_path, 'r') as file:
            log_content = file.read()
            # Here, implement your logic for analyzing the application logs
            # For simplicity, let's just return the first 100 characters
            return log_content[:100]
    except FileNotFoundError:
        return "Application log file not found."
    except Exception as e:
        return str(e)

# log_analysis/application.py
from django.conf import settings
import re
from datetime import datetime
from collections import defaultdict

def analyze_application_logs(log_content):
    # Define a pattern that matches the various application log entries
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) UserID=(?P<userid>\w+) Action=(?P<action>[A-Za-z]+) (DocumentID=(?P<documentid>\d+))? Status=(?P<status>\w+)(?: Reason=(?P<reason>[\w\s]+))?'
    
    action_counts = defaultdict(int)
    status_counts = defaultdict(int)
    user_actions = defaultdict(lambda: defaultdict(int))
    document_access = defaultdict(lambda: defaultdict(int))
    
    lines = log_content.split('\n')
    for line in lines:
        if line.strip():  # Ensure the line is not empty
            match = re.match(pattern, line)
            if match:  # If the line matches the pattern
                parsed_line = match.groupdict()
                action = parsed_line['action']
                status = parsed_line['status']
                userid = parsed_line['userid']
                documentid = parsed_line.get('documentid')
                
                action_counts[action] += 1
                status_counts[status] += 1
                user_actions[userid][action] += 1
                
                if documentid:
                    document_access[documentid][status] += 1
    
    analysis_results = {
        'action_counts': dict(action_counts),
        'status_counts': dict(status_counts),
        'user_actions': {user: dict(actions) for user, actions in user_actions.items()},
        'document_access': {doc: dict(access) for doc, access in document_access.items()},
    }
    
    return analysis_results

# from django.http import HttpResponse
# def test_log_path(request):
#     app_log_path = settings.LOG_FILE_PATHS.get('application')
#     # Print the path to the console
#     print(app_log_path)
#     # Also return it as an HTTP response for testing
#     return HttpResponse(f"Application Log Path: {app_log_path}")

# def analyze_application_logs():
#     log_file_path = settings.LOG_FILE_PATHS.get('application')
#     try:
#         with open(log_file_path, 'r') as file:
#             log_content = file.read()
#             # Here, implement your logic for analyzing the application logs
#             # For simplicity, let's just return the first 100 characters
#             return log_content[:100]
#     except FileNotFoundError:
#         return "Application log file not found."
#     except Exception as e:
#         return str(e)
# def analyze_application_logs(log_content):
#     # Here, implement your logic for analyzing the application logs
#     # For simplicity, let's just return the first 100 characters of log_content
#     return log_content[:100]
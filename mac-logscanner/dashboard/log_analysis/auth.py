# log_analysis/auth.py
from django.conf import settings
import re
from datetime import datetime
from collections import defaultdict


# def analyze_auth_logs():
#     log_file_path = settings.LOG_FILE_PATHS.get('auth')
#     try:
#         with open(log_file_path, 'r') as file:
#             log_content = file.read()
#             # Here, implement your logic for analyzing the auth logs
#             # For simplicity, let's just return the first 100 characters
#             return log_content[:100]
#     except FileNotFoundError:
#         return "auth log file not found."
#     except Exception as e:
#         return str(e)


# test log_analysis/auth.py
# def analyze_auth_logs(log_content):
#     # Initialize counters
#     success_count = 0
#     failure_count = 0
    
#     # Split log content into lines
#     lines = log_content.split('\n')
    
#     for line in lines:
#         if 'status=success' in line:
#             success_count += 1
#         elif 'status=failure' in line:
#             failure_count += 1
    
#     # Compile analysis results
#     analysis_results = {
#         'success_count': success_count,
#         'failure_count': failure_count,
#     }
#     return analysis_results
# def analyze_auth_logs(log_content):
#     # Here, implement your logic for analyzing the auth logs
#     # For simplicity, let's just return the first 100 characters of log_content
#     return log_content[:100]


# def analyze_auth_logs(log_content):
#     # Define the regular expression pattern for parsing log lines
#     pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) User login attempt: username=(?P<username>\w+) status=(?P<status>\w+)(?: reason=(?P<reason>[\w\s]+))?'
    
#     # Initialize counters and a dictionary for failure reasons
#     success_count = 0
#     failure_count = 0
#     failed_login_reasons = {}

#     # Split log content into lines
#     lines = log_content.split('\n')
#     for line in lines:
#         if line.strip():  # Skip empty lines
#             match = re.match(pattern, line)
#             if match:
#                 parsed_line = match.groupdict()
#                 # Increment counters based on status
#                 if parsed_line['status'] == 'success':
#                     success_count += 1
#                 elif parsed_line['status'] == 'failure':
#                     failure_count += 1
#                     # Aggregate reasons for failed logins
#                     reason = parsed_line.get('reason', 'Unknown')
#                     failed_login_reasons[reason] = failed_login_reasons.get(reason, 0) + 1

#     # Compile and return analysis results as a dictionary
#     analysis_results = {
#         'success_count': success_count,
#         'failure_count': failure_count,
#         'failed_login_reasons': failed_login_reasons
#     }
#     return analysis_results


# def analyze_auth_logs(log_content):
#     # Enhanced regular expression pattern to include IP addresses
#     pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) User login attempt: username=(?P<username>\w+) status=(?P<status>\w+)(?: reason=(?P<reason>[\w\s]+))?'
    
#     # Initialize additional counters and structures
#     ip_attempts = defaultdict(int)
#     user_attempts = defaultdict(int)
#     commonly_exploited_usernames = {'admin', 'administrator', 'root'}
#     exploited_username_attempts = 0

#     # Define a threshold for identifying suspicious activity
#     threshold = 5  # Adjust based on your analysis or dynamic criteria

#     # Initialize counters for success and failure
#     success_count = 0
#     failure_count = 0
#     failed_login_reasons = {}
#     timestamps = []
#     intervals_per_user = {}
    
#     lines = log_content.split('\n')
#     for line in lines:
#         if line.strip():
#             match = re.match(pattern, line)
#             if match:
#                 parsed_line = match.groupdict()
#                 timestamp = datetime.strptime(parsed_line['timestamp'], '%Y-%m-%d %H:%M:%S')
#                 timestamps.append(timestamp)

#                 ip_attempts[parsed_line['ip']] += 1
#                 user_attempts[parsed_line['username']] += 1
                
#                 if parsed_line['username'].lower() in commonly_exploited_usernames:
#                     exploited_username_attempts += 1
                
#                 if parsed_line['status'] == 'success':
#                     success_count += 1
#                 elif parsed_line['status'] == 'failure':
#                     failure_count += 1
#                     reason = parsed_line.get('reason', 'Unknown')
#                     failed_login_reasons[reason] = failed_login_reasons.get(reason, 0) + 1
                    
#                     # Calculate interval since last attempt for each user
#                     if len(timestamps) > 1:
#                         interval = (timestamp - timestamps[-2]).total_seconds()
#                         intervals_per_user[parsed_line['username']].append(interval)

#     # Process and compile analysis results
#     average_intervals_per_user = {user: sum(intervals) / len(intervals) for user, intervals in intervals_per_user.items() if intervals}
#     suspicious_ips = {ip for ip, count in ip_attempts.items() if count > threshold}
#     suspicious_users = {user for user, count in user_attempts.items() if count > threshold}

    
#     analysis_results = {
#         'success_count': success_count,
#         'failure_count': failure_count,
#         'failed_login_reasons': failed_login_reasons,
#         'average_intervals_per_user': average_intervals_per_user,
#         'suspicious_ips': suspicious_ips,
#         'suspicious_users': suspicious_users,
#         'exploited_username_attempts': exploited_username_attempts,
#     }
#     return analysis_results
from collections import defaultdict
from datetime import datetime

def analyze_auth_logs(log_content):
    # Enhanced regular expression pattern to include IP addresses
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) User login attempt: username=(?P<username>\w+) status=(?P<status>\w+)(?: reason=(?P<reason>[\w\s]+))?'
    
    # Initialize additional counters and structures
    ip_attempts = defaultdict(int)
    user_attempts = defaultdict(int)
    commonly_exploited_usernames = {'admin', 'administrator', 'root'}
    exploited_username_attempts = 0

    # Initialize counters for success and failure
    success_count = 0
    failure_count = 0
    failed_login_reasons = {}
    timestamps = []
    intervals_per_user = {}
    
    # Process each line of the log content
    lines = log_content.split('\n')
    for line in lines:
        if line.strip():  # Ensure the line is not empty
            match = re.match(pattern, line)
            if match:  # If the line matches the pattern
                parsed_line = match.groupdict()
                timestamp = datetime.strptime(parsed_line['timestamp'], '%Y-%m-%d %H:%M:%S')
                timestamps.append(timestamp)

                ip_attempts[parsed_line['ip']] += 1
                user_attempts[parsed_line['username']] += 1
                
                # Check for commonly exploited usernames
                if parsed_line['username'].lower() in commonly_exploited_usernames:
                    exploited_username_attempts += 1
                
                # Count successes and failures
                if parsed_line['status'] == 'success':
                    success_count += 1
                elif parsed_line['status'] == 'failure':
                    failure_count += 1
                    # Collect reasons for failures
                    reason = parsed_line.get('reason', 'Unknown')
                    failed_login_reasons[reason] = failed_login_reasons.get(reason, 0) + 1
                    
                    # Calculate the interval since the last attempt for each user
                    if len(timestamps) > 1:
                        interval = (timestamp - timestamps[-2]).total_seconds()
                        if parsed_line['username'] not in intervals_per_user:
                            intervals_per_user[parsed_line['username']] = []
                        intervals_per_user[parsed_line['username']].append(interval)

    # Compile the analysis results
    analysis_results = {
        'success_count': success_count,
        'failure_count': failure_count,
        'failed_login_reasons': failed_login_reasons,
        'average_intervals_per_user': {user: sum(intervals) / len(intervals) for user, intervals in intervals_per_user.items() if intervals},
        'exploited_username_attempts': exploited_username_attempts,
        'ip_attempts': dict(ip_attempts),
        'user_attempts': dict(user_attempts),
        'commonly_exploited_usernames': list(commonly_exploited_usernames),
    }
    
    # Removed the suspicious_ips and suspicious_users from the results as threshold logic is removed
    return analysis_results
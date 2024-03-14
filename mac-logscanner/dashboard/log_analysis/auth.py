
from django.conf import settings
from datetime import datetime
from collections import defaultdict
import re

def analyze_auth_logs(log_content):
    ip_attempts = defaultdict(int)
    user_failures = defaultdict(int)
    timestamps = defaultdict(list)
    ip_user_attempts = defaultdict(lambda: defaultdict(int))  # Tracks login attempts per user per IP for Credential Stuffing detection
    account_enumeration = defaultdict(lambda: {'success': 0, 'failure': 0, 'first_success': None})  # Correctly defined here
    
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) User login attempt: username=(?P<username>\w+) status=(?P<status>\w+)(?: reason=(?P<reason>[\w\s]+))?'

    detected_vulnerabilities = defaultdict(lambda: {"type": [], "description": []})

    lines = log_content.split('\n')
    for line in lines:
        if line.strip():
            match = re.match(pattern, line)
            if match:
                parsed_line = match.groupdict()
                timestamp = datetime.strptime(parsed_line['timestamp'], '%Y-%m-%d %H:%M:%S')
                ip_attempts[parsed_line['ip']] += 1
                timestamps[parsed_line['username']].append(timestamp)
                ip_user_attempts[parsed_line['ip']][parsed_line['username']] += 1
                if parsed_line['status'] == 'failure':
                    user_failures[parsed_line['username']] += 1
                    account_enumeration[parsed_line['username']]['failure'] += 1  # Update failure count
                else:
                    if not account_enumeration[parsed_line['username']]['first_success']:
                        account_enumeration[parsed_line['username']]['first_success'] = timestamp
                    account_enumeration[parsed_line['username']]['success'] += 1  # Update success count

    # Brute Force Attack Detection
    for user, count in user_failures.items():
        if count > 6:  # Adjust based on log volume and expected behavior
            detected_vulnerabilities[user]["type"].append("Brute Force Attack")
            detected_vulnerabilities[user]["description"].append("Numerous failed login attempts indicating a possible brute force attack.")

    # Credential Stuffing Detection
    for ip, users_attempts in ip_user_attempts.items():
        if len(users_attempts) > 5:  # Indicates attempts across multiple accounts
            detected_vulnerabilities[ip]["type"].append("Credential Stuffing")
            detected_vulnerabilities[ip]["description"].append("Failed login attempts across multiple usernames from the same IP address, suggesting credential stuffing.")

    # Account Enumeration Detection
    for user, info in account_enumeration.items():
        if info['failure'] > 8 and info['first_success']:  # Adjust threshold as needed
            detected_vulnerabilities[user]["type"].append("Account Enumeration")
            detected_vulnerabilities[user]["description"].append("Multiple failed login attempts before a successful login, indicating potential account enumeration.")

    # Consolidating results into a more informative structure
    analysis_results = {
        'ip_attempts': dict(ip_attempts),
        'user_failures': dict(user_failures),
        'detected_vulnerabilities': {user: {
                                        "vulnerabilities": detected_vulnerabilities[user]["type"],
                                        "descriptions": detected_vulnerabilities[user]["description"]
                                        } for user in detected_vulnerabilities}
    }

    return analysis_results
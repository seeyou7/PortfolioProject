from django.conf import settings
from datetime import datetime
from collections import defaultdict
import re

def analyze_auth_logs(log_content):
    ip_attempts = defaultdict(int)
    user_failures = defaultdict(int)
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) User login attempt: username=(?P<username>\w+) status=(?P<status>\w+)(?: reason=(?P<reason>[\w\s]+))?'
    detected_vulnerabilities = defaultdict(lambda: {"type": [], "description": []})

    lines = log_content.split('\n')
    for line in lines:
        if line.strip():
            match = re.match(pattern, line)
            if match:
                parsed_line = match.groupdict()
                ip_attempts[parsed_line['ip']] += 1
                if parsed_line['status'] == 'failure':
                    user_failures[parsed_line['username']] += 1

    # BR Detection
    for user, count in user_failures.items():
        if count > 6:  # A AJUSTER SELON LA TAILLE DU LOG 
            detected_vulnerabilities[user]["type"].append("Brute Force Attack")
            detected_vulnerabilities[user]["description"].append("Numerous failed login attempts indicating a possible brute force attack.")

    # Consolider le results into a more informative structure
    analysis_results = {
        'ip_attempts': dict(ip_attempts),
        'user_failures': dict(user_failures),
        'detected_vulnerabilities': {user: {
            "vulnerabilities": detected_vulnerabilities[user]["type"],
            "descriptions": detected_vulnerabilities[user]["description"]
        } for user in detected_vulnerabilities}
    }

    return analysis_results

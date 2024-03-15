from django.conf import settings
import re
from datetime import datetime
from collections import defaultdict


def analyze_application_logs(log_content):
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<src_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) SrcPort=(?P<src_port>\d+) DestIP=(?P<dest_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) DestPort=(?P<dest_port>\d+) Action=(?P<action>\w+) (Payload="(?P<payload>.+?)")? Status=(?P<status>\w+)(?: Reason=(?P<reason>.+))?'
    
    sql_injection_attempts = []
    
    lines = log_content.split('\n')
    for line in lines:
        if line.strip():
            match = re.match(pattern, line)
            if match:
                parsed_line = match.groupdict()
                
                # Check for SQL Injection in the payload
                if "SELECT" in parsed_line.get('payload', '') and "--" in parsed_line.get('payload', ''):
                    sql_injection_attempts.append(parsed_line)

    sql_injection_description = (
    "SQL Injection Description:\n"
    "SQL Injection (SQLi) is a common attack vector that exploits vulnerabilities\n"
    "in an application's software by manipulating SQL queries. This can allow\n"
    "attackers to view, modify, delete, or create data in the database without\n"
    "authorization. SQLi attacks can lead to significant breaches, including data\n"
    "loss, data theft, and loss of data integrity. Mitigation strategies include\n"
    "validating and sanitizing all user inputs, using prepared statements with\n"
    "parameterized queries, and employing ORM frameworks that reduce the risk of SQLi.\n"
    "www.google.com "
).strip()

  
    # Compilation of analysis results
    analysis_results = {
        'sql_injection_attempts': sql_injection_attempts,
    }

    # Including the SQL injection description only if SQL injection attempts are detected
    if sql_injection_attempts:
        analysis_results['sql_injection_description'] = sql_injection_description
    
    return analysis_results

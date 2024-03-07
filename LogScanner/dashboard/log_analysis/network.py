from django.conf import settings
import re
from collections import defaultdict
from django.conf import settings
from datetime import datetime


def analyze_network_logs(log_content):
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<src_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) SrcPort=(?P<src_port>\d+) DestIP=(?P<dest_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) DestPort=(?P<dest_port>\d+) Action=(?P<action>\w+) (Payload="(?P<payload>.+?)")? Status=(?P<status>\w+)(?: Reason=(?P<reason>.+))?'

    ddos_attempts = defaultdict(int)
    sql_injection_attempts = []
    
    lines = log_content.split('\n')
    for line in lines:
        if line.strip():
            match = re.match(pattern, line)
            if match:
                parsed_line = match.groupdict()
                if parsed_line['dest_port'] == '80':
                    ddos_attempts[parsed_line['dest_ip']] += 1
                
                if "SELECT" in parsed_line.get('payload', '') and "--" in parsed_line.get('payload', ''):
                    sql_injection_attempts.append(parsed_line)
    
    # Analyzer  DDoS en  counting requests per destination IP ca  marche pour le moment
    potential_ddos = {dest_ip: count for dest_ip, count in ddos_attempts.items() if count > threshold}  
    
    #compilation (ok)
    analysis_results = {
        'potential_ddos': potential_ddos,
        'sql_injection_attempts': sql_injection_attempts,
    }
    
    return analysis_results

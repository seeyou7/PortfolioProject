from django.conf import settings
import re
from collections import defaultdict
from django.conf import settings

def analyze_network_logs(log_content, ddos_threshold=100, unauthorized_endpoints=["/admin", "/login"]):
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<src_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) SrcPort=(?P<src_port>\d+) DestIP=(?P<dest_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) DestPort=(?P<dest_port>\d+) Action=(?P<action>\w+) (Payload="(?P<payload>.+?)")? Status=(?P<status>\w+)(?: Reason=(?P<reason>.+))?'
    
    ddos_attempts = defaultdict(int)
    unauthorized_access_attempts = defaultdict(int)
    
    lines = log_content.split('\n')
    for line in lines:
        if line.strip():
            match = re.match(pattern, line)
            if match:
                parsed_line = match.groupdict()
                
                # Counting DDoS attempts per destination IP
                ddos_attempts[parsed_line['dest_ip']] += 1
                
                # Detecting Unauthorized Access attempts
                for endpoint in unauthorized_endpoints:
                    if endpoint in parsed_line.get('payload', ''):
                        unauthorized_access_attempts[parsed_line['dest_ip']] += 1
    
    # Identifying potential DDoS attacks
    potential_ddos = {dest_ip: count for dest_ip, count in ddos_attempts.items() if count >= ddos_threshold}
    
    # Identifying potential Unauthorized Access
    potential_unauthorized_access = {dest_ip: count for dest_ip, count in unauthorized_access_attempts.items() if count > 0}
    
    analysis_results = {
        'potential_ddos': potential_ddos,
        'unauthorized_access_attempts': potential_unauthorized_access,
    }
    
    # Check if any vulnerabilities were detected
    if not potential_ddos and not potential_unauthorized_access:
        print("No network vulnerabilities found.")
    else:
        print("Network vulnerabilities detected:")
        if potential_ddos:
            print("Potential DDoS attacks detected.")
        if potential_unauthorized_access:
            print("Potential Unauthorized Access detected.")
    
    return analysis_results

















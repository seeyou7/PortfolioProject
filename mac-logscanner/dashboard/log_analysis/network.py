from django.conf import settings
import re
from collections import defaultdict
from django.conf import settings

def analyze_network_logs(log_content, ddos_threshold=100,):
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<src_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) SrcPort=(?P<src_port>\d+) DestIP=(?P<dest_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) DestPort=(?P<dest_port>\d+) Action=(?P<action>\w+) (Payload="(?P<payload>.+?)")? Status=(?P<status>\w+)(?: Reason=(?P<reason>.+))?'

    ddos_attempts = defaultdict(int)


    lines = log_content.split('\n')
    for line in lines:
        if line.strip():
            match = re.match(pattern, line)
            if match:
                parsed_line = match.groupdict()
                
                # Counting DDoS attempts par destination IP
                ddos_attempts[parsed_line['dest_ip']] += 1
                
              
    # Identifying potential DDoS attacks
    potential_ddos = {dest_ip: count for dest_ip, count in ddos_attempts.items() if count >= ddos_threshold}
    
      
    # Compile analysis results
    vulnerabilities_detected = potential_ddos 
    analysis_results = {
        'potential_ddos': potential_ddos,
        'vulnerabilities_detected': vulnerabilities_detected,
        'summary': "Network vulnerabilities detected." if vulnerabilities_detected else "No network vulnerabilities found."
    }
    
    return analysis_results
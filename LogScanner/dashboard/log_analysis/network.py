# log_analysis/network.py
from django.conf import settings

def analyze_network_logs():
    log_file_path = settings.LOG_FILE_PATHS.get('network')
    try:
        with open(log_file_path, 'r') as file:
            log_content = file.read()
            # Here, implement your logic for analyzing the network logs
            # For simplicity, let's just return the first 100 characters
            return log_content[:100]
    except FileNotFoundError:
        return "network log file not found."
    except Exception as e:
        return str(e)

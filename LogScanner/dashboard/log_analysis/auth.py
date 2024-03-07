
from django.conf import settings
import requests
import re
from datetime import datetime
from collections import defaultdict, Counter
import numpy as np
from pyod.models.knn import KNN


def query_nvd_for_vulnerabilities(indicators):
    nvd_search_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    matched_vulnerabilities = []

    for indicator in indicators:
        query_params = {"keyword": indicator}
        response = requests.get(nvd_search_url, params=query_params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            try:
                vulnerabilities = response.json().get('result', {}).get('CVE_Items', [])
                matched_vulnerabilities.extend(vulnerabilities)
            except ValueError as e:
                print(f"Error parsing JSON: {e}")
                print(f"Response Text: {response.text}")
        else:
            print(f"Failed to query NVD: {response.text}")

    return matched_vulnerabilities

def analyze_auth_logs(log_content):
    # Initialize dictionaries for analysis
    ip_attempts = defaultdict(int)
    user_failures = defaultdict(int)
    timestamps = defaultdict(list)
    
    # Regular regex expression for log parsing
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) IP=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) User login attempt: username=(?P<username>\w+) status=(?P<status>\w+)(?: reason=(?P<reason>[\w\s]+))?'
    
    # traiter log lines
    lines = log_content.split('\n')
    for line in lines:
        if line.strip():
            match = re.match(pattern, line)
            if match:
                parsed_line = match.groupdict()
                timestamp = datetime.strptime(parsed_line['timestamp'], '%Y-%m-%d %H:%M:%S')
                ip_attempts[parsed_line['ip']] += 1
                timestamps[parsed_line['username']].append(timestamp)
                if parsed_line['status'] == 'failure':
                    user_failures[parsed_line['username']] += 1

    # Analysis for outlier detection
    ip_attempt_values = np.array(list(ip_attempts.values())).reshape(-1, 1)
    outlier_ips = []
    if ip_attempt_values.shape[0] > 1:
        ip_model = KNN(n_neighbors=min(5, len(ip_attempt_values)-1))
        ip_model.fit(ip_attempt_values)
        ip_outliers = ip_model.labels_ == 1
        outlier_ips = [ip for ip, outlier in zip(ip_attempts.keys(), ip_outliers) if outlier]

    failure_values = np.array(list(user_failures.values())).reshape(-1, 1)
    outlier_users_by_failures = []
    if failure_values.shape[0] > 1:
        failure_model = KNN(n_neighbors=min(5, len(failure_values)-1))
        failure_model.fit(failure_values)
        failure_outliers = failure_model.labels_ == 1
        outlier_users_by_failures = [user for user, outlier in zip(user_failures.keys(), failure_outliers) if outlier]

    # Combiner les indicators and query NVD
    indicators = outlier_ips + outlier_users_by_failures
    vulnerabilities_matched = query_nvd_for_vulnerabilities(indicators)

    # Compiler analysis results
    analysis_results = {
        'ip_attempts': dict(ip_attempts),
        'user_failures': dict(user_failures),
        'outlier_ips': outlier_ips,
        'outlier_users_by_failures': outlier_users_by_failures,
        'matched_vulnerabilities': vulnerabilities_matched,
    }

    return analysis_results
    
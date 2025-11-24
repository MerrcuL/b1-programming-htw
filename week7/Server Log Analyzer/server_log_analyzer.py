import re
import logging
from datetime import datetime
from collections import defaultdict, Counter

# Initialize Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('week7/Server Log Analyzer/analysis_audit.log'),
        logging.StreamHandler()
    ]
)

class ServerLogAuditor:
    def __init__(self, target_file):
        self.filepath = target_file
        # Regex to capture: IP, Timestamp, Method, URL, Status Code, Bytes
        self.parser_regex = re.compile(
            r'(\S+) - - \[(.*?)\] "(\S+) (\S+) \S+" (\d+) (\d+)'
        )
        
        # Data Containers
        self.stats = {
            'total_hits': 0,
            'visitors': set(),
            'methods': Counter(),
            'endpoints': Counter(),
            'codes': Counter()
        }
        
        # Error Tracking
        self.http_errors = []
        
        # Security Tracking
        self.auth_failures = defaultdict(list)
        self.denied_access_events = []
        self.threat_log = []
        
        # Definitions for security scanning
        self.sql_signatures = ['union', 'select', 'drop', 'insert', '--', ';']

    def _extract_data(self, raw_line):
        """Extracts structured data from a raw log line."""
        search_result = self.parser_regex.match(raw_line)
        if not search_result:
            return None
            
        host, time_str, method, uri, status_code, byte_size = search_result.groups()
        
        return {
            'remote_host': host,
            'time': time_str,
            'req_method': method,
            'resource': uri,
            'code': int(status_code),
            'bytes': int(byte_size)
        }

    def _scan_threats(self, record):
        """Evaluates a log record for potential security risks."""
        host = record['remote_host']
        resource = record['resource']
        
        # 1. Check for Brute Force (401 on /login)
        if resource == '/login' and record['code'] == 401:
            self.auth_failures[host].append(record['time'])
            
            # Trigger alert on 3rd failure
            if len(self.auth_failures[host]) >= 3:
                fail_count = len(self.auth_failures[host])
                alert_msg = (f"Brute force detected: {host} - "
                             f"{fail_count} failed attempts")
                self.threat_log.append(alert_msg)
                logging.warning(alert_msg)

        # 2. Check for Forbidden Access (403)
        if record['code'] == 403:
            alert_msg = f"Access Forbidden: {host} attempted -> {resource}"
            self.denied_access_events.append(alert_msg)
            self.threat_log.append(alert_msg)
            logging.warning(alert_msg)

        # 3. Check for SQL Injection signatures
        uri_lower = resource.lower()
        if any(sig in uri_lower for sig in self.sql_signatures):
            alert_msg = f"SQL Injection Suspected: {host} -> {resource}"
            self.threat_log.append(alert_msg)
            logging.warning(alert_msg)

    def execute_audit(self):
        """Main execution loop to read and process the log file."""
        logging.info(f"Initiating audit for: {self.filepath}")
        
        try:
            with open(self.filepath, 'r') as file_handle:
                for idx, raw_text in enumerate(file_handle, 1):
                    try:
                        data = self._extract_data(raw_text.strip())
                        if not data:
                            logging.debug(f"Skipping malformed line #{idx}")
                            continue

                        # Increment General Statistics
                        self.stats['total_hits'] += 1
                        self.stats['visitors'].add(data['remote_host'])
                        self.stats['methods'][data['req_method']] += 1
                        self.stats['endpoints'][data['resource']] += 1
                        self.stats['codes'][data['code']] += 1

                        # Log HTTP Errors (4xx/5xx)
                        if data['code'] >= 400:
                            self.http_errors.append(data)

                        # Run Security Checks
                        self._scan_threats(data)

                    except Exception as err:
                        logging.error(f"Processing error on line {idx}: {err}")
                        continue
                        
            logging.info(f"Audit finished. Total records: {self.stats['total_hits']}")

        except FileNotFoundError:
            logging.error(f"Critical: File '{self.filepath}' does not exist.")
            raise
        except PermissionError:
            logging.error(f"Critical: Permission denied for '{self.filepath}'.")
            raise

    def write_summary(self):
        """Creates the general statistical overview file."""
        try:
            with open('week7/Server Log Analyzer/summary_report.txt', 'w') as report:
                self._write_header(report, "SERVER TRAFFIC ANALYSIS")
                
                report.write("TRAFFIC METRICS\n")
                report.write("-" * 60 + "\n")
                report.write(f"Total Hits:      {self.stats['total_hits']}\n")
                report.write(f"Unique Visitors: {len(self.stats['visitors'])}\n\n")
                
                report.write("HTTP METHOD BREAKDOWN\n")
                for method, count in self.stats['methods'].most_common():
                    report.write(f" {method:<10}: {count}\n")
                    
                report.write("\nTOP 5 ENDPOINTS\n")
                for uri, count in self.stats['endpoints'].most_common(5):
                    report.write(f" {uri}: {count} hits\n")
                    
                report.write("\nSTATUS CODES\n")
                for code, count in sorted(self.stats['codes'].items()):
                    report.write(f" {code}: {count}\n")
                    
                report.write("\n" + "=" * 60 + "\n")
            logging.info("Report generated: summary_report.txt")
        except PermissionError:
            logging.error("Failed to write summary_report.txt")

    def write_security_brief(self):
        """Creates the security incident report."""
        try:
            with open('week7/Server Log Analyzer/security_incidents.txt', 'w') as report:
                self._write_header(report, "SECURITY THREAT ASSESSMENT")
                
                report.write(f"Total Incidents Logged: {len(self.threat_log)}\n\n")
                
                report.write("REPEATED AUTH FAILURES\n")
                report.write("-" * 60 + "\n")
                for host, attempts in self.auth_failures.items():
                    if len(attempts) >= 3:
                        report.write(f"Host: {host} | Failures: {len(attempts)}\n")
                        
                report.write("\nACCESS DENIED LOG\n")
                report.write("-" * 60 + "\n")
                for event in self.denied_access_events:
                    report.write(f"{event}\n")
                    
                report.write("\nCHRONOLOGICAL INCIDENT LOG\n")
                report.write("-" * 60 + "\n")
                for incident in self.threat_log:
                    report.write(f"{incident}\n")
                    
                report.write("\n" + "=" * 60 + "\n")
            logging.info("Report generated: security_incidents.txt")
        except PermissionError:
            logging.error("Failed to write security_incidents.txt")

    def write_error_log(self):
        """Exports all 4xx/5xx errors to a separate file."""
        try:
            with open('week7/Server Log Analyzer/error_log.txt', 'w') as report:
                self._write_header(report, "HTTP ERROR REGISTRY")
                report.write(f"Count: {len(self.http_errors)}\n\n")
                
                for err in self.http_errors:
                    line = (f"[{err['time']}] {err['remote_host']} | "
                            f"{err['req_method']} {err['resource']} | "
                            f"Code: {err['code']}\n")
                    report.write(line)
                    
                report.write("\n" + "=" * 60 + "\n")
            logging.info("Report generated: error_log.txt")
        except PermissionError:
            logging.error("Failed to write error_log.txt")

    @staticmethod
    def _write_header(file_obj, title):
        """Helper to write consistent headers."""
        file_obj.write("=" * 60 + "\n")
        file_obj.write(f"{title}\n")
        file_obj.write("=" * 60 + "\n\n")

def main():
    auditor = ServerLogAuditor('week7/Server Log Analyzer/server.log')
    
    try:
        # Execute Processing
        auditor.execute_audit()
        
        # Generate Outputs
        auditor.write_summary()
        auditor.write_security_brief()
        auditor.write_error_log()
        
        # Console Summary
        print("\n--- Audit Completed Successfully ---")
        print(f"Processed: {auditor.stats['total_hits']} lines")
        print(f"Threats:   {len(auditor.threat_log)}")
        print(f"Errors:    {len(auditor.http_errors)}")
        print("\nOutput Files:")
        print(" 1. summary_report.txt")
        print(" 2. security_incidents.txt")
        print(" 3. error_log.txt")
        print(" 4. analysis_audit.log")
        
    except Exception as e:
        logging.critical(f"System Failure: {e}")
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    main()
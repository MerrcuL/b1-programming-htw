import datetime

class Device:
    def __init__(self, device_id, device_type, owner, firmware_version="1.0"):
        self.device_id = device_id
        self.device_type = device_type
        self.owner = owner
        self.firmware_version = firmware_version
        self.__compliance_status = True 
        self.__is_active = True            
        self.last_security_scan = datetime.datetime.now()
    
        if not device_id or not device_type:
             raise ValueError("Device ID and Type cannot be empty.")

    def authorise_access(self, user):        
        self._log(f"Access request by {user.username}")

        if not self.__is_active:
            print("Access DENIED: Device is quarantined or inactive.")
            return False

        is_compliant = self.check_compliance()

        if user.privilege_level == 'admin':
            if not is_compliant:
                self._log(f"Admin {user.username} overrode compliance check.")
            return True

        if user.username == self.owner:
            if is_compliant:
                return True
            else:
                print("Access DENIED: Device is non-compliant.")
                return False
        
        print("Access DENIED: Unauthorised user.")
        return False

    def check_compliance(self):
        days_since_scan = (datetime.datetime.now() - self.last_security_scan).days
        
        if days_since_scan > 30:
            self.__compliance_status = False
            self._log("Compliance check FAILED: Scan overdue.")
        else:
            self.__compliance_status = True
            
        return self.__compliance_status

    def run_security_scan(self):
        print(f"Running security scan on {self.device_id}...")
        self.last_security_scan = datetime.datetime.now()
        self.__compliance_status = True
        self._log("Security scan completed. Device is now compliant.")

    def update_firmware(self, new_version):
        self.firmware_version = new_version
        self._log(f"Firmware updated to {new_version}")

    def quarantine_device(self):
        self.__is_active = False
        self.__compliance_status = False
        self._log("Device QUARANTINED due to security threat.")

    def _log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[DEVICE LOG] {timestamp} | ID: {self.device_id} | {message}")


class DeviceManager:
    def __init__(self):
        self.devices = {}

    def add_device(self, device):
        if device.device_id in self.devices:
            print("Error: Device ID already exists.")
        else:
            self.devices[device.device_id] = device
            print(f"Device {device.device_id} added to registry.")

    def remove_device(self, device_id):
        if device_id in self.devices:
            del self.devices[device_id]
            print(f"Device {device_id} removed.")

    def generate_security_report(self):
        print("\n--- NETWORK SECURITY REPORT ---")
        for d_id, device in self.devices.items():
            status = "Compliant" if device.check_compliance() else "NON-COMPLIANT"
            print(f"ID: {d_id} | Owner: {device.owner} | Status: {status} | FW: {device.firmware_version}")
        print("-------------------------------")
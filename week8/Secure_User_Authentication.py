import hashlib

class User:
    
    def __init__(self, username, password_hash, privilege_level, status="active"):
        self.username = username
        self.__login_attempts = 0
        self.__password_hash = password_hash
        self.__privilege_level = privilege_level
        self.__status = status
 
    @property
    def status(self):
        return self.__status
    
    @property
    def privilege_level(self):
        return self.__privilege_level
    
    @privilege_level.setter
    def privilege_level(self, new_level):
        self._validate_privilege(new_level)
        self.__privilege_level = new_level
        self.log_activity(f"Privilege level changed to {new_level}")
    
    def _validate_privilege(self, level):
        valid_levels = ['user', 'moderator', 'admin']
        if level not in valid_levels:
            raise ValueError(f"Invalid privilege level: {level}")
            
    def authenticate(self, input_password):   
        if self.status == 'locked':
            print(f"Login denied. Account {self.username} is locked.")
            return False
        
        input_hash = hashlib.sha256(input_password.encode()).hexdigest()

        if self.__password_hash == input_hash:
            self.reset_login_attempts()
            self.log_activity("Successful login")
            return True
        else:
            self.__login_attempts += 1
            self.log_activity(f"Failed login attempt ({self.__login_attempts})")
            
            if self.__login_attempts >= 3:
                self.lock_account()
            return False
    def check_privileges(self, required_privilege):
        if self.__privilege_level == 'admin':
            return True
        return self.__privilege_level == required_privilege
    
    def lock_account(self):
        self.__status = 'locked'
        self.log_activity("ACCOUNT LOCKED due to security violation")


    def reset_login_attempts(self):        
        self.__login_attempts = 0

    def log_activity(self, activity):
        print(f"[LOG] User: {self.username} | Action: {activity}")

    def display_user_info(self):
        print(f"User Profile: {self.username}")
        print(f"Role: {self.__privilege_level}")
        print(f"Status: {self.__status}")


# Testing the implementation
print("Creating User...")
# Create a user (using a fake hash for demonstration)
user1 = User("j_doe", "f916d6f557982ee5277be921a2675190d2d02e88782db7409223a53c7c84b9ba", "standard")
print("User created.")

print("\n--- Testing Failed Login Logic ---")
# [cite: 42] Account locking after failed login attempts
user1.authenticate("wrong_hash") # Attempt 1
user1.authenticate("wrong_hash") # Attempt 2
user1.authenticate("SuperSecurePass123") # Attempt 3 (Should lock)

print("\n--- Testing Lockout ---")
# [cite: 96] Non-compliant/Locked devices denied access
# Even with correct password, it should now fail
user1.authenticate("secret_hash_123") 

print("\n--- Testing Safe Display ---")
#  Display info without sensitive data
user1.display_user_info()


print("\n--- Testing Encapsulation ---")
try:
    # [cite: 47] Direct manipulation of password fields prevented
    print(user1.__password_hash) 
except AttributeError:
    print("Success: Direct access to private password variable was blocked.")
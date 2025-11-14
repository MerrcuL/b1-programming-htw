passwords = [ "Pass123",
"SecurePassword1", "weak",
"MyP@ssw0rd", "NOLOWER123"]

stats = [0, 0]

def is_valid_password(password):
    check_result = f"FAIL: \"{password}\" - "
    has_upper = any(c.isupper() for c in password)
    if not has_upper:
        check_result += "Password must contain at least one uppercase letter. "
    has_lower = any(c.islower() for c in password)
    if not has_lower:
        check_result += "Password must contain at least one lowercase letter. "
    has_digit = any(c.isdigit() for c in password)
    if not has_digit:
        check_result += "Password must contain at least one digit. "
    if len(password) < 8:
        check_result += "Password must be at least 8 characters long. "
    if has_upper and has_lower and has_digit and len(password) >= 8:
        check_result = f"PASS: \"{password}\" is valid."
        stats[1] += 1
    else:
        stats[0] += 1
    print(check_result)

for password in passwords:
    is_valid_password(password)

print(f"Password validation complete! {stats[1]} compliant, {stats[0]} non-compliant passwords.")

import string
import random

def check_min_length(password, min_length=8):
    return len(password) >= min_length
def check_uppercase(password):
    return any(c.isupper() for c in password)
def check_lowercase(password):
    return any(c.islower() for c in password)
def check_digit(password):
    return any(c.isdigit() for c in password)
def has_special_char(password, special_chars="!@#$%^&*"):
    return any(c in special_chars for c in password)
def validate_password(password):
    checks = {"Minimum Length": check_min_length(password),
              "Has Uppercase": check_uppercase(password),
              "Has Lowercase": check_lowercase(password),
              "Has Digit": check_digit(password),
              "Has special character": has_special_char(password)}
    is_valid = all(checks.values())
    return checks, is_valid 
encouraging_messages = [
    "Keep going, you're making great progress!",
    "Every step forward counts, no matter how small.",
    "Believe in yourself—you’ve got what it takes.",
    "You’re stronger than you think.",
    "Don’t give up; success is closer than you realize.",
    "Mistakes are proof that you’re trying.",
    "Stay positive—good things take time.",
    "You’re doing better than you think.",
    "Keep pushing forward; your effort will pay off.",
    "One day at a time, one step at a time.",
    "Trust the process and keep moving.",
    "You’ve overcome challenges before; you can do it again.",
    "Focus on progress, not perfection.",
    "Your determination will get you through this.",
    "Believe in your vision—even when it’s tough.",
    "Stay consistent; effort builds results.",
    "You're capable, resilient, and growing stronger every day.",
    "Challenges are opportunities in disguise.",
    "You have every reason to be proud of yourself.",
    "Keep your head up—better days are ahead."
]
def get_random_encouragement():
    return random.choice(encouraging_messages)
password = input("Please rype in a password to validate: ")
checks, is_valid = validate_password(password)
print("Password Validation Results:")
for check, passed in checks.items():
    status = "Met" if passed else "Not met"
    print(f"{check} - {status}")
if is_valid:
    print("\nThe password is strong.")
else:
    print("\nThe password is weak.\nHere is an encouraging message for you:")
    print(get_random_encouragement())
login_attempts = [
    ("alice", "success"),
    ("bob", "failed"),
    ("bob", "failed"),
    ("charlie", "success"),
    ("bob", "failed"),
    ("alice", "failed")]


failed_attempts = {}

for i in range(len(login_attempts)):
    username, status = login_attempts[i]
    if status == "failed":
        if username in failed_attempts:
            failed_attempts[username] += 1
        else:
            failed_attempts[username] = 1

print("Checking login attempts...")

for user in failed_attempts:
    if failed_attempts[user] >= 3:
        print(f"ALERT: User \"{user}\" has {failed_attempts[user]} failed login attempts.")

print("Security check complete!")
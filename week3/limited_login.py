pin = "1984"
attempts = 3
while attempts > 0:
    user_input = input("Please enter your PIN: ")
    if user_input == pin:
        print("Access granted.")
        break
    else:
        attempts -= 1
        if attempts > 0:
            print(f"Incorrect PIN. You have {attempts} attempts left.")
        else:
            print("Access denied. No attempts left.")
            
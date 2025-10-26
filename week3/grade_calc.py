score = int(input("Please enter your score (0-100): "))
if score < 0 or score > 100:
    print("Invalid score. Please enter a score between 0 and 100.")
    exit()
elif score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'
print(f"Your final grade is: {grade}")

if grade == 'A':
    print("You are  doing great!")
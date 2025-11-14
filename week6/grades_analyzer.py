def get_letter_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

students_records = []
stats = {"highest": None, "lowest": None, "average": 0, "median": 0}
gradde_distribution = {}
scores = []
unique_scores = set()

for i in range(6):
    record_input = input(f"Enter record {i+1}: ")
    name, score_str = record_input.split(' ')
    score = int(score_str)
    scores.append(score)
    students_records.append((name, score))
    if score in gradde_distribution:
        gradde_distribution[score] += 1
    else:
        gradde_distribution[score] = 1

stats["highest"] = max(scores)
stats["lowest"] = min(scores)
stats["average"] = sum(scores) / len(scores)
unique_scores = set(scores)

scores_sorted = sorted(scores)
n = len(scores_sorted)
if n % 2 == 1:
    stats["median"] = scores_sorted[n // 2]
else:
    stats["median"] = (scores_sorted[n // 2 - 1] + scores_sorted[n // 2]) / 2

print("\n=== STUDENT RECORDS ===")
for i in range(len(students_records)):
    name, score = students_records[i]
    print(f"{i+1}. {name}: {score} ({get_letter_grade(score)})")

print("\n=== CLASS STATISTICS ===")
print(f"Highest Score: {stats['highest']}")
print(f"Lowest Score: {stats['lowest']}")
print(f"Average Score: {stats['average']:.2f}")
print(f"Median Score: {stats['median']}")

print("\n=== UNIQUE SCORES ===")
print(sorted(unique_scores))
print(f"Total unique scores: {len(unique_scores)}")

print("\n=== GRADE DISTRIBUTION ===")
sorted_grades = sorted(gradde_distribution.items(), key=lambda x: (-x[1], -x[0]))
for score, count in sorted_grades:
    student_word = "student" if count == 1 else "students"
    print(f"Score {score}: {count} {student_word}")

print("\nThank you for using the Grades Analyzer!")
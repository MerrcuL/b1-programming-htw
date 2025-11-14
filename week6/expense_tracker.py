expense_records = []
category_totals = {}
unique_categories = set()
overall_stats = {
    "total_expense": 0, 
    "average_expense": 0,
    "highest_expense": 0, 
    "lowest_expense": 0, 
    "highest_expense_category": None, 
    "lowest_expense_category": None, 
    "highest_expense_date": None, 
    "lowest_expense_date": None
    }

num_records = int(input("How many expense records would you like to enter? Enter a number: "))

for i in range(num_records):
    record_input = input(f"Enter expense record {i+1} (format: category amount date[YYYY-MM-DD]): ")
    category, amount_str, date = record_input.split(' ')
    amount = float(amount_str)
    expense_records.append((category, amount, date))
    
    overall_stats["total_expense"] += amount

    if overall_stats["highest_expense"] < amount:
        overall_stats["highest_expense"] = amount
        overall_stats["highest_expense_category"] = category
        overall_stats["highest_expense_date"] = date
    if overall_stats["lowest_expense"] == 0 or amount < overall_stats["lowest_expense"]:
        overall_stats["lowest_expense"] = amount
        overall_stats["lowest_expense_category"] = category
        overall_stats["lowest_expense_date"] = date

overall_stats["average_expense"] = overall_stats["total_expense"] / len(expense_records)

for record in expense_records:
    category, amount, date = record
    unique_categories.add(category)
    if category in category_totals:
        category_totals[category] += amount
    else:
        category_totals[category] = amount

print("\n---- OVERALL SPENDING SUMMARY ----")
print(f"Total Spending: ${overall_stats['total_expense']:.2f}")
print(f"Average Expense: ${overall_stats['average_expense']:.2f}")
print(f"Highest Expense: ${overall_stats['highest_expense']:.2f} (Category: {overall_stats['highest_expense_category']}, Date: {overall_stats['highest_expense_date']})")
print(f"Lowest Expense: ${overall_stats['lowest_expense']:.2f} (Category: {overall_stats['lowest_expense_category']}, Date: {overall_stats['lowest_expense_date']})")

print("\n---- UNIQUE CATEGORIES SPENT ON ----")
print(unique_categories)
print(f"Total unique categories: {len(unique_categories)}")

print("\n---- SPENDING BY CATEGORY ----")
for category in category_totals:
    print(f"{category}: ${category_totals[category]:.2f}")

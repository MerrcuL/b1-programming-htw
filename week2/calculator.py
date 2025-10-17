''' 
A functional calculator that accepts user input, performs calculations, 
and displays formatted results with proper error handling and documentation
'''

revenue = float(input("Enter revenue: "))
costs = float(input("Enter costs: "))

profit = revenue - costs
profit_margin = (revenue - costs) / revenue * 100 if revenue != 0 else 0


print("\n--- Financial Summary ---")
print(f"Revenue: ${revenue:,.2f}")
print(f"Costs: ${costs:,.2f}")
print(f"Profit: ${profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")

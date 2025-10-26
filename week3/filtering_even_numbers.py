nums = input("Input the list of numbers separated by ' ': ").split(' ')
even_nums = []
for num in nums:
    if int(num) % 2 == 0:
        even_nums.append(num)

print("Even numbers:", ', '.join(even_nums))
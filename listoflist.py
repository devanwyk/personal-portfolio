fruits = ["apple", "orange", "banana", "coconut"]
vegetables = ["carrot", "broccoli", "asparagus"]
meat = ["chicken", "pork", "beef"]

groceries = [fruits, vegetables, meat]



for food in groceries:
    for item in food:
        print(item, end=" ")
    print()


num_pad = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ('*',0,'#'))

for row in num_pad:
    for key in row:
        print(key, end=" ")
    print()
    
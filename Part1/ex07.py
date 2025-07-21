# Dictionary containing names and ages
age = {'Hans': 24, 'Prag': 23, 'Bunyod': 18}

# 1. Print the whole dictionary
print("Whole dictionary:", age)

# 2. Print the age of 'Hans'
print("Age of Hans:", age['Hans'])

# 3. Change the age of 'Prag' to 30
age['Prag'] = 30

# 4. Print the updated age of 'Prag'
print("Updated age of Prag:", age['Prag'])

# 5. Delete key-value pair of 'Bunyod' from the dictionary
del age['Bunyod']

# 6. Print the updated dictionary
print("Updated dictionary:", age)
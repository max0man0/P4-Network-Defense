from csv import reader

# Read the CSV file
with open('tests.csv', 'r') as file:
    csv_reader = reader(file)
    # Read the first 50 rows
    # for i in range(50):
    #     print(next(csv_reader))
    true = 0
    false = 0
    for row in csv_reader:
        if row[-1] == 'False':
            false += 1
        else:
            true += 1
    total = true + false
    print(f"Total: {total}")
    print(f"True: {true}")
    print(f"False: {false}")
        
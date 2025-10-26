import pandas as pd
import numpy as np  


print(pd.__version__)
print(np.__version__)

line_break: str = "*" * 20

print(line_break)


data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [24, 27, 22, 32],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

data2 = [100, 102, 104, 106, 200, 202, 204, 206]
series = pd.Series(data2)
series2 = pd.Series(data2, index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], name='Sample Series')


print(f'{series = }')
print(f'{series2 = }')

print(f'{series2.loc["c"] = }') # Access by label
print()
print(f'{series2.iloc[0] = }') # Access by position
print()
print(line_break)

print()
# Boolean indexing for index less than 200
print(f'{series2[series2 < 200] = }')  # Boolean indexing

# Boolean indexing for index greater than or equal  200
print(f'{series2[series2 >= 200] = }')  # Boolean indexing 



print(line_break)


calories = { "DAY 1": 1750, "DAY 2": 2100, "DAY 3": 1700 }
series = pd.Series(calories)
print(f'{series = }')

# Update the value for "DAY 3" by 500 calories
series.loc["DAY 3"] += 500

print("After increasing DAY 3 by 500 calories:")
print(f'{series = }')
print()
# Update the value for "DAY 3" by decreased by 500 calories
series.loc["DAY 3"] -= 500  
print("After decreasing DAY 3 by 500 calories:")
print(f'{series = }')


print(line_break)



print()

df = pd.DataFrame(data, index=["Employee 1", "Employee 2", "Employee 3", "Employee 4"])
print(f'{df.loc["Employee 2"] = }')
print()

print(line_break)


#df = pd.DataFrame(data, columns=['Name', 'Age', 'City'])
#print(f'{df = }')

#print(f'{df.loc["Name"] = }')  # Access row by label (index 1)

#Add a new column "Job" to the DataFrame
df['Job'] = ['Engineer', 'Doctor', 'Artist', 'Lawyer']  

print("After adding 'Job' column:")
print(df)

print()


print(line_break)

# create 2 rows with Sally and Mark with index Employee 5 and Employee 6

new_rows = pd.DataFrame({
    'Name': ['Sally', 'Mark'],
    'Age': [29, 35],
    'City': ['San Francisco', 'Seattle'],
    'Job': ['Designer', 'Architect']
}, index=["Employee 5", "Employee 6"])

df = pd.concat([df, new_rows])

print("After adding new rows for Sally and Mark:")
print(df)
print()
print(line_break)

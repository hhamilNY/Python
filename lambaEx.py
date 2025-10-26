# Lambda Functions = A small anonymous function
# Can take any number of arguments, but can only have one expression
# Often used as a quick throw-away function
# Syntax: lambda arguments: expression
# Helps keep the namespace clean and is useful with higher order functions 
# like map(), filter(), sorted(), sort() and reduce()

line_break: str = "-" * 30


# Example 1: A lambda function that adds 10 to the input argument
add_10 = lambda x: x + 10   
print(f'add_10(5) = {add_10(5)}')  # Output: 15
print(line_break)
# Example 2: A lambda function that multiplies two arguments
multiply = lambda x, y: x * y
print(f'multiply(2, 3) = {multiply(2, 3)}')  # Output: 6
print(line_break)
# Example 3: A lambda function used with the map() function to square each number in a list
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f'squared = {squared}')  # Output: [1, 4, 9, 16, 25]
print(line_break)
# Example 4: A lambda function used with the filter() function to get even numbers from a list
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f'even_numbers = {even_numbers}')  # Output: [2, 4]
print(line_break)
# Example 5: A lambda function used with the sorted() function to sort a list of tuples by the second element
tuples = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
sorted_tuples = sorted(tuples, key=lambda x: x[1])
print(f'sorted_tuples = {sorted_tuples}')  # Output: [(4, 'four'), (1, 'one'), (3, 'three'), (2, 'two')]
print(line_break)
# Example 6: A lambda function used with reduce() to compute the product of a list of numbers
from functools import reduce
product = reduce(lambda x, y: x * y, numbers)
print(f'product = {product}')  # Output: 120
print(line_break)
# Example 7: A lambda function used to create a simple function that returns the length of a string
length = lambda s: len(s)
print(f'length("Hello") = {length("Hello")}')  # Output: 5
print(line_break)
print()
# Example 8: A lambda function used with pandas to create a new column in a DataFrame   
import pandas as pd
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
df = pd.DataFrame(data)
df['Age_in_5_years'] = df['Age'].apply(lambda x: x + 5)
print(df)
print(line_break)
print() 
# Example 9: A lambda function used with pandas to filter rows in a DataFrame
filtered_df = df[df['Age'].apply(lambda x: x > 28)]
print(filtered_df)
print(line_break)
print()
# Example 10: A lambda function used with pandas to sort a DataFrame by a custom key
sorted_df = df.sort_values(by='Name', key=lambda x: x.str.len())
print(sorted_df)
print(line_break)
print()
# Example 11: A lambda function used with pandas to group data and apply a custom aggregation
grouped_df = df.groupby('Age').agg({'Name': lambda x: ', '.join(x)})
print(grouped_df)
print(line_break)
print()
# Example 12: A lambda function used with pandas to create a new column based on multiple columns
df['Name_Age'] = df.apply(lambda row: f"{row['Name']} is {row['Age']} years old", axis=1)
print(df)
print(line_break)
print() 
# Example 13: A lambda function used with pandas to normalize a numeric column
df['Normalized_Age'] = df['Age'].apply(lambda x: (x - df['Age'].min()) / (df['Age'].max() - df['Age'].min()))
print(df)
print(line_break)
print()
# Example 14: A lambda function used with pandas to categorize ages into groups
df['Age_Group'] = df['Age'].apply(lambda x: 'Young' if x < 30 else 'Old')
print(df)
print(line_break)
print()
# Example 15: A lambda function used with pandas to calculate the square of ages
df['Age_Squared'] = df['Age'].apply(lambda x: x ** 2)
print(df)
print(line_break)
print()
# Example 16: A lambda function used with pandas to find the maximum age in the DataFrame
max_age = df['Age'].apply(lambda x: x).max()
print(f'Maximum Age: {max_age}')
print(line_break)
print()
# Example 17: A lambda function used with pandas to find the minimum age in the DataFrame
min_age = df['Age'].apply(lambda x: x).min()
print(f'Minimum Age: {min_age}')
print(line_break)
print()
# Example 18: A lambda function used with pandas to calculate the average age in the DataFrame
average_age = df['Age'].apply(lambda x: x).mean()
print(f'Average Age: {average_age}')
print(line_break)
print()
# Example 19: A lambda function used with pandas to count the number of unique names in
# the DataFrame
unique_names_count = df['Name'].apply(lambda x: x).nunique()
print(f'Number of Unique Names: {unique_names_count}')
print(line_break)
print()
# Example 20: A lambda function used with pandas to create a Series and update values
series = pd.Series({'DAY 1': 300, 'DAY 2': 400, 'DAY 3': 500, 'DAY 4': 600})
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
# Example 21: A lambda function used with pandas to create a DataFrame and add new rows and columns
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}
df_new = pd.DataFrame(data)
print(f'{df_new = }')
# Add a new column 'Age in 10 years' using a lambda function
df_new['Age_in_10_years'] = df_new['Age'].apply(lambda x: x + 10)
print("After adding 'Age_in_10_years' column:")
print(df_new)
print()
print(line_break)
# Add new rows for 'Sally' and 'Mark'
new_rows = pd.DataFrame({
    'Name': ['Sally', 'Mark'],
    'Age': [29, 35],
    'City': ['San Francisco', 'Seattle']
}, index=["Employee 5", "Employee 6"])
df_new = pd.concat([df_new, new_rows], ignore_index=True)
print("After adding new rows for Sally and Mark:")
print(df_new)
print()
print(line_break)
print()
# End of lambdaEx.py





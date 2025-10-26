import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


print(pd.__version__)
print(np.__version__)
line_break: str = "*" * 20

df =pd.read_csv("data_panda.csv")
print()
print(line_break)


# Data Cleaning = The process of identifying and correcting (or removing) errors, inconsistencies, and inaccuracies in data to improve its quality and reliability for analysis.
# ~75% of work done withPandas is data cleaning

# Drop irreleveant columns
df_cleaned = df.drop(columns=["Legendary", "No"])
print("After dropping 'Legendary' and 'No' columns:")
print(f'{df_cleaned.to_string() }')


print()
print(line_break)

# Handle missing Data naan

# df = df.dropna(subset=["Type2"]) # Drop rows where 'Type2' is NaN
# print("After dropping rows with NaN in 'Type2':")
# print(f'{df.to_string() }')

# print()
# print(line_break)

# # Fill missing data
# df = df.fillna({"Type2": "None"}) # Fill rows where 'Type2' is NaN
# print("After filling rows with NaN in 'Type2':")
# print(f'{df.to_string() }')

print()
print(line_break)

# Fix inconsistemy Values 

df["Type1"] = df["Type1"].replace({"Grass": "GRASS", 
                                   "Fire": "FIRE",
                                   "Water": "WATER"}) # Correct misspelled 'Grass' to 'GRASS'

print("After fixing inconsistencies in 'Type1':")
print(f'{df.to_string() }')


# Fix Data types 

print()
print(line_break)

df["Legendary"] = df["Legendary"].astype(bool) # Convert 'Legendary' column to boolean type
print("After converting 'Legendary' to boolean type:")
print(f'{df.to_string() }')

print()
print(line_break)

# Remove Duplicates
df = df.drop_duplicates(subset=["Name", "Type1", "Type2"]) # Remove duplicate rows based on 'Name', 'Type1', and 'Type2'
print("After removing duplicates based on 'Name', 'Type1', and 'Type2':")
print(f'{df.to_string() }')
print()
print(line_break)
# Data Transformation = The process of converting data from one format or structure into another to make it more suitable for analysis or processing.
# Common transformations include normalization, aggregation, pivoting, and encoding categorical variables.      
# Normalize numerical columns (e.g., Height and Weight) to a 0-1 scale
df["Height_Norm"] = (df["Height"] - df["Height"].min()) / (df["Height"].max() - df["Height"].min())
df["Weight_Norm"] = (df["Weight"] - df["Weight"].min()) / (df["Weight"].max() - df["Weight"].min())
print("After normalizing 'Height' and 'Weight':")
print(f'{df.to_string() }')
print()
print(line_break)
# Encode categorical variables (e.g., Type1 and Type2) using one-hot encoding
df_encoded = pd.get_dummies(df, columns=["Type1", "Type2"], prefix=["Type1", "Type2"])
print("After one-hot encoding 'Type1' and 'Type2':")
print(f'{df_encoded.to_string() }')
print()
print(line_break)
# Aggregate data: Calculate average Height and Weight by Type1
df_agg = df.groupby("Type1").agg(
{"Height": "mean", "Weight": "mean"}).reset_index()
print("Average Height and Weight by Type1:")
print(f'{df_agg.to_string() }')
print()
print(line_break)
# Pivot data: Create a pivot table showing average Height by Type1 and Type2
df_pivot = df.pivot_table(values="Height", index="Type1", columns="Type2", aggfunc="mean")
print("Pivot table of average Height by Type1 and Type2:")
print(f'{df_pivot.to_string() }')
print()
print(line_break)
# Sort data: Sort by Height descending
df_sorted = df.sort_values(by="Height", ascending=False)
print("Data sorted by Height descending:")
print(f'{df_sorted.to_string() }')
print()
print(line_break)
# Filter data: Select rows where Weight > 100
df_filtered = df[df["Weight"] > 100]


print("Rows where Weight > 100:")
print(f'{df_filtered.to_string() }')
print()
print(line_break)
# Reset index after filtering
df_filtered = df_filtered.reset_index(drop=True)

print("Filtered data with reset index:")
print(f'{df_filtered.to_string() }')
print()
print(line_break)
# Rename columns for clarity
df_renamed = df.rename(columns={"Type1": "Primary_Type", "Type2": "Secondary_Type"})
print("Data with renamed columns:")
print(f'{df_renamed.to_string() }')
print()
print(line_break)
# Working with Series
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [28, 34, 29, 42],
    "City": ["New York", "Los Angeles", "Chicago", "Houston"]
}

# Create a DataFrame from the data
df_series = pd.DataFrame(data)

# Display the DataFrame
print("DataFrame created from Series:")
print(f'{df_series.to_string() }')
print()
print(line_break)

# Accessing Series
print("Accessing individual Series:")
print(f"Name Series:\n{df_series['Name']}")
print(f"Age Series:\n{df_series['Age']}")
print(f"City Series:\n{df_series['City']}")
print()
print(line_break)

# Modifying Series
df_series['Age'] = df_series['Age'] + 1  # Increment age by 1
print("After modifying 'Age' Series:")
print(f'{df_series.to_string() }')
print()
print(line_break)

# Filtering Series
df_filtered_series = df_series[df_series['Age'] > 30]
print("Filtered Series (Age > 30):")
print(f'{df_filtered_series.to_string() }')
print()
print(line_break)
# Series operations
df_series['Age_Squared'] = df_series['Age'] ** 2
print("After adding 'Age_Squared' Series:")
print(f'{df_series.to_string() }')
print()
print(line_break)
# Summary statistics on Series
print("Summary statistics on 'Age' Series:")
print(f"Mean Age: {df_series['Age'].mean()}")
print(f"Max Age: {df_series['Age'].max()}")
print(f"Min Age: {df_series['Age'].min()}")
print()
print(line_break)
# Handling missing data in Series
df_series_with_nan = df_series.copy()
df_series_with_nan.loc[2, 'City'] = None  # Introduce a NaN value
print("Series with NaN value:")

print(f'{df_series_with_nan.to_string() }')
print()
print(line_break)
df_series_filled = df_series_with_nan.fillna({'City': 'Unknown'})
print("After filling NaN in 'City' Series:")
print(f'{df_series_filled.to_string() }')
print()
print(line_break)
# Series aggregation
print("Series aggregation on 'Age' Series:")
print(f"Total Age: {df_series['Age'].sum()}")

print(f"Average Age: {df_series['Age'].mean()}")
print()
print(line_break)
# Series sorting
df_series_sorted = df_series.sort_values(by='Age', ascending=False)
print("Series sorted by 'Age' descending:")
print(f'{df_series_sorted.to_string() }')
print()
print(line_break)
# Series indexing
print("Accessing Series using .loc and .iloc:")

print(f"Using .loc to access first row:\n{df_series.loc[0]}")
print(f"Using .iloc to access first row:\n{df_series.iloc[0]}")
print()
print(line_break)
# Boolean indexing
print("Boolean indexing on 'Age' Series:")

print(f'{df_series[df_series["Age"] < 30] = }')  # Age less than 30
print(f'{df_series[df_series["Age"] >= 30] = }')  # Age greater than or equal to 30
print()

print(line_break)



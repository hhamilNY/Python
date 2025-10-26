import pandas as pd 
import numpy as np


print(pd.__version__)
print(np.__version__)

# aggregate functions = Reduces a set of values into a single summary value. Used to summarize and analyze data
# Often used with groupby() def name(args):


line_break: str = "*" * 20

df =pd.read_csv("data_panda.csv")

# whole dataframe
#



# print("df.mean")
# print (f'{df.mean(numeric_only=True)  }')  # Mean of numeric columns

# print("df.sum")
# print(f'{df.sum(numeric_only=True)  }')    # Sum of numeric columns
# print("df.std()")
# print(f'{df.std(numeric_only=True)  }')    # Standard deviation of numeric columns
# print("df.min")
# print(f'{df.min(numeric_only=True) }')    # Minimum of numeric columns
# print("df.max")
# print(f'{df.max(numeric_only=True) }')    # Maximum of numeric columns
# print("df.count")
# print(f'{df.count() }')                 # Count of non-NA/null entries

print()
print(line_break)
print(f'df.describe')
print(f'{df.describe() }')                # Summary statistics for numeric columns

                
# single Column 
print()
print(line_break)  
print('df["Height"].mean()')
print(f'{df["Height"].mean() }')                # Summary statistics for a single column

print()
print(line_break)  
print(f'df["Height"].sum()')
print(f'{df["Height"].sum() }')              # Summary statistics for a single column

print()
print(line_break)  
print(f'df["Height"].min()')
print(f'{df["Height"].min() }') 
    
print()
print(line_break)  
print(f'df["Height"].max()')
print(f'{df["Height"].max() }')

print()
print(line_break)  
print(f'df["Height"].count()')
print(f'{df["Height"].count() }')




print()
print(line_break)

# GroupBy operations

group = df.groupby("Type1")

print(f'group["Height"].max()')
print(f'{group["Height"].max() }')

print()
print(line_break)

print(f'group["Height"].count()')
print(f'{group["Height"].count() }')
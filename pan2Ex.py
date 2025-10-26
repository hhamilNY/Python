import pandas as pd
import numpy as np

print(pd.__version__)
print(np.__version__)
line_break: str = "*" * 20
print(line_break)

df = pd.read_json("data_panda.json")
print(df.to_string())

print(line_break)

df = pd.read_csv("data_panda.csv", index_col="Name")
print(df.to_string())
print(line_break)


print(line_break)


#print(df["Name"].to_string())
#print(df["Height"].to_string())
#print(df["Weight"].to_string())

# Selection by Column
#print(df[["Name", "Height", "Weight"]].to_string()) # can be used when trying row lookup - renove idex_col above

print(line_break)
print() 
# Selection by Row(s)
print(df.loc["Pikachu"].to_string())
print(line_break)
print(df.loc["Pikachu"])
print()
print(line_break)
print(df.loc["Charizard"])


print()
print(line_break)
print(df.loc["Bulbasaur":"Squirtle"])  # Range of rows from Bulbasaur to Squirtle inclusive 

print()
print(line_break)
print(df.loc["Charizard" , [ "Height", "Weight"]])  # Specific row and specific columns


print()
print(line_break)
print(df.iloc[0:11:2, 0:3])  # Rows from 0 to 10 with step 2, and columns from 0 to 2
print()
print(line_break)

pokemon = input("Enter a Pokemon name: ")

try:
  print(df.loc[pokemon])
except KeyError:
  print(f'KeyError: {pokemon} not found')
except Exception:
  print('Some other exception occurred')


print()
print(line_break)

# filtering = Keeping the rows that match a coniition of Height over 1.9
filtered_df = df[df["Height"] > 1.9]

print(filtered_df.to_string())

print()
print(line_break)


ff_pokemon = df[(df["Type1"] =="Fire" ) & 
                (df["Type2"] == "Flying")]

print(ff_pokemon.to_string())

print()
print(line_break)


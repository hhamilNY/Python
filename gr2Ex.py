from itertools import groupby 
from typing import Any, Iterator


words: list[str] = ['Cat', 'Catcus', 'Owl', 'Dog,', 'Orange', 'Bob', 'Blue']
grouped_words: groupby = groupby(sorted(words), key=lambda s: s[0])

for letter, group in grouped_words:
    print(f'Starts with "{letter}": {list(group)}')

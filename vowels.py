def vowels(text: str) -> int:
    return sum(1 for char in text if char.lower() in 'aeiou')


def count_vowels(text: str) -> int:
    """

    Counts the total vowels of any given text. 

    :param text: the text to count the vowels in. 
    :return: the total vowel count as an integer


    """
    if not isinstance(text, str):
        raise TypeError(f'Please only use strings, {type(text)} is not a valid type.')


    vowel_count: int = 0
    vowels: str = "aeiouAEIOU"  
    for char in text:
       if char in vowels:
           vowel_count += 1
    return vowel_count


line_break: str = '-' * 40


def main() -> None:
   #sample_text: str = "Hello, World!"
   sample_text: str =  'I shower with a cowboy hat so my sunglasses don\'t get wet.'
   result: int = count_vowels(sample_text)

   print(line_break)
   print(f'Number of vowels in "{sample_text}": {result}')
   print(line_break)
   print(f'Number of vowels in "{sample_text}": {vowels(sample_text)}')
   print(line_break)

if __name__ == "__main__":
   main()

from random import  sample



for i in range(1, 6):
    lotto: list[int] = sample(range(1,70), 5)
    #lotto.sort()
    magic: list[int] = sample(range(1,27), 1)
    print(f'Winners: #{i} lotto=  {sorted(lotto)} {magic=}')


    

import asyncio 

line_break: str = '-' * 25

async def fetch_data(special_item: str):
    print('start fetching')
    await asyncio.sleep(2)
    print('done fetching')
    return{'data': special_item}

async def print_numbers(num: float):
    for i in range(10):
        print(i)
        await asyncio.sleep(num) # you can vary the time and it will alter the results


async def main():
    task1 = asyncio.create_task(fetch_data('Diana')) 
    task2 = asyncio.create_task(print_numbers(.25)) 

    value = await task1

    print(f'{value =}')
    await task2

    print(line_break)

    task3 = asyncio.create_task(fetch_data('Jack')) 
    task4 = asyncio.create_task(print_numbers(.5)) 

    valueA = await task3

    print(f'{valueA =}')
    await task4




asyncio.run(main()) 


           
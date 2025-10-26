import asyncio 

async def set_future_result(future, value):
    
    await asyncio.sleep(2)  # Simulate some async operation
    future.set_result(value)
    print(f'Future result set to: {value}')

async def main():
    #Create a future object
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    #Set the future result in a separate task
    asyncio.create_task(set_future_result(future, "Future result is ready"))

    print('Waiting for future result...')

    await asyncio.sleep(1)  # Simulate some other async operation
    #Wait for the future to be resolved
    result = await future
    print(f'Main received future result: {result}')

if __name__ == "__main__":
    asyncio.run(main())
    

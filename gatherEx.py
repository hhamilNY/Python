import asyncio 

async def fetch_data(id,sleep_time):
    print(f"Coroutine started for ID {id}") 
    await asyncio.sleep(sleep_time)
    return {"id": id, "data": f"Data for ID {id}"}

async def main():
    #Run coroutines concurrently and gather their return ValuesView
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 1),
        fetch_data(3, 3)
    )

   
    print("All coroutines completed.")
    print("Results:")
    for result in results:
        print(f"Result for ID {result['id']}: {result['data']}")
        print("Coroutine completed.")

if __name__ == "__main__":
    asyncio.run(main())

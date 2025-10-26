import asyncio 


async def fetch_data(id, sleep_time):
    print(f"Coroutine started for ID {id}") 
    await asyncio.sleep(sleep_time)
    return {"id": id, "data": f"Data for ID {id}"}


async def main():
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for i, sleep_time in enumerate([2, 1, 3], start =1):
            task =tg.create_task(fetch_data(i, sleep_time))
            tasks.append(task)
    print("All coroutines completed.")
    print("Results:")

    #After the Task Group block, all tasks have completed
    for result in tasks:
        print(f"Result for ID {result.result()['id']}: {result.result()['data']}")


if __name__ == "__main__":
    asyncio.run(main())     
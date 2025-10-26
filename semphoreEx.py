import asyncio 

async def access_resource(semaphore, resource_id):
    print(f"Task {resource_id} is waiting to access the resource.")
    async with semaphore:
        print(f"Task {resource_id} has acquired the semaphore.")
        # Simulate some processing time
        await asyncio.sleep(1)
        print(f"Task {resource_id} is releasing the semaphore.")


async def main():
    # Create a semaphore that allows up to 2 concurrent accesses
    semaphore = asyncio.Semaphore(2)

    # Create multiple tasks that will try to access the shared resource
   
    #tasks = [access_resource(semaphore, i) for i in range(5)]
    await asyncio.gather(*(access_resource(semaphore, i) for i in range(5)))

    # Run the tasks concurrently
    # 
if __name__ == "__main__":
    asyncio.run(main())
     
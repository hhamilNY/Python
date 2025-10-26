import asyncio 

# A Shared variable
shared_resource = 0

# A Lock to control access to the shared resource
lock = asyncio.Lock()   

async def modify_shared_resource():
    global shared_resource
    async with lock:
        # Critical section starts
        print(f"shared resource value before modification : {shared_resource}")
        shared_resource += 1 #modify the shared resource    
        # Simulate some processing time
        await asyncio.sleep(1)
        print(f"Shared resource modified to: {shared_resource}")
        #Critical section ends 

async def main():
    await asyncio.gather(*(modify_shared_resource() for _ in range(5)))



if __name__ == "__main__":
    asyncio.run(main()) 

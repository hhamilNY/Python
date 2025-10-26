import asyncio 

async def waiter(event):
    print("Waiting for the event to be set...")
    await event.wait()
    print("Event has been set! Continuing execution.")

async def setter(event):
    print("Setting the event in 2 seconds...")
    await asyncio.sleep(2)
    event.set()
    print("Event is set. Continue the execution ...")

async def main():
    event = asyncio.Event()
    await asyncio.gather(waiter(event), setter(event))


if __name__ == "__main__":
    asyncio.run(main()) 
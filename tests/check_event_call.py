import asyncio
from src import discord_bot

# this test tries to see of the check_events function works properly.
# to do so, change the data.json when the check_events will run. you can see if its working by the output of the bot

async def run_check():

    await asyncio.sleep(4)

    while True:
        await discord_bot.client.check_events()
        await asyncio.sleep(20)


async def main():

    run_bot = asyncio.create_task(discord_bot.run_bot())
    check_task = asyncio.create_task(run_check())

    await asyncio.gather(run_bot, check_task)

if __name__ == "__main__":
    asyncio.run(main())
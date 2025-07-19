from src.web_scrapper import web_scrapper
import src.discord_bot as bot
import asyncio

scrapper = web_scrapper()
loop = asyncio.new_event_loop()
event = asyncio.Event()

async def run_scrapper(scrapper):
    await asyncio.sleep(4)
    while True:

        print("pegando informações...")
        driver = scrapper.start_browser()
        participants = scrapper.get_information(driver)
        information = scrapper.sort_participants(participants)
        scrapper.save_JSON(information)
        await bot.client.check_events()
        await asyncio.sleep(300)

async def main():

    scrapper_task = asyncio.create_task(run_scrapper(scrapper))
    bot_task = asyncio.create_task(bot.run_bot())

    await asyncio.gather(bot_task, scrapper_task)

if __name__ == "__main__":
    asyncio.run(main())
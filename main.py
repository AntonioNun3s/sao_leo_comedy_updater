from src.web_scrapper import web_scrapper
import src.discord_bot as bot
import asyncio

scrapper = web_scrapper()
loop = asyncio.new_event_loop()
event = asyncio.Event()

# run the scrapper methods and the bot updater every 5 minutes

async def run_scrapper(scrapper):
    await asyncio.sleep(4)
    while True:

        print("pegando informações...")
        driver = scrapper.start_browser()
        participants = scrapper.get_information(driver)
        information = scrapper.filter_participants(participants)
        scrapper.save_JSON(information)
        await bot.client.check_events()
        await asyncio.sleep(300)

# creates a main function where it can run both the bot and the scrapper methods

async def main():

    scrapper_task = asyncio.create_task(run_scrapper(scrapper))
    bot_task = asyncio.create_task(bot.run_bot())

    await asyncio.gather(bot_task, scrapper_task)

if __name__ == "__main__":
    asyncio.run(main())
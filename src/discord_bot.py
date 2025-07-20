import discord
import json

class MyClient(discord.Client):

    # we create some variables to use inside the bot. we create a information variable to store the JSON and the channel_ID to store the ID

    with open("data/data.json", "r", encoding="utf-8") as file:
        json_str = file.read()
        info = json.loads(json_str)
        information = info
    channel_ID = 000000 # channel ID here

    # prints out when bot is ready

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    # checks if theres a new event or if an event has 1 day left before the show

    async def check_events(self):
        
        channel = self.get_channel(self.channel_ID)

        with open("data/data.json", "r", encoding="utf-8") as file:
            json_str = file.read()
            temp_info = json.loads(json_str)

            for participant in temp_info:
                idx = temp_info.index(participant)

                # on this if statement, we check the new artist on the page. so, we compare the name of the artist with the old json of the bot
                # if its different, it notifies that theres a new show
                # but it would also trigger the other participants names, since each artist of the new json moves one index.
                # so, to fix that, we also compare the next item in the bot json and compare its name with the new json.
                # if the new participant is diferent than the mirror index and the next bot index, then its a new artist and then the bots print it out
                # also, we use the line "idx + 1 == len(temp_info)"" to prevent out of range error

                if participant["name"] != self.information[idx]["name"] and (idx + 1 == len(temp_info) or participant["name"] != self.information[idx+1]["name"]):
                    output = "NOVO SHOW!\n " + participant["name"] + " IRA SE APRESENTAR DIA " + participant["date"] + " AS " + participant["time"]
                    try:
                        await channel.send(output)
                        print(output)
                    except discord.HTTPException as e:
                        print(f"Error sending message: {e}")
                
            for participant in temp_info:

                # almost same logic from the other if statement. but on this one, we look each participant that has less than 1 day of time until the show
                # after that, we see if it was already been notified that theres 1 day left for the show with the line:
                # participant["days_for_the_show"] != self.information[idx]["days_for_the_show"]
                # if its diferent, then it notifies that theres 1 day left for the show
                # but it would also trigger if a new artist gets inserted in the json. since each index moves by one, it would also change the "days_for_the_show"
                # to fix that, we check if both participant from the bot and the new json have the same name. if they do, then the "days_for_the_show" really changed
                # if they do, then the "days_for_the_show" really changed and then the bot prints it out

                if participant["days_for_the_show"] == 0:
                    idx = temp_info.index(participant)

                    if participant["days_for_the_show"] != self.information[idx]["days_for_the_show"] and participant["name"] == self.information[idx]["name"]:
                        output = "FALTA 1 DIA PARA O EVENTO DO/A " + participant["name"] + " NO DIA " + participant["date"] + " AS " + participant["time"]
                        try:
                            await channel.send(output)
                            print(output)
                        except discord.HTTPException as e:
                            print(f"Error sending message: {e}")
            

            # saves the new JSON on the information variable

            self.information = temp_info

# bot object. it gets assigned with the MyClient object in the run_bot function

client = None

# we put the MyClient object to run on this function so we can async it with the scrapper object and its methods

async def run_bot():

    intents = discord.Intents.default()
    intents.message_content = True

    global client

    client = MyClient(intents=intents)
    await client.start('bot-token-here')
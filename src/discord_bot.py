import discord
import json

class MyClient(discord.Client):

    information = None
    channel = 0000000 # channel ID here

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def check_events(self):
        send_channel = self.get_channel(self.channel)
        
        with open("sao_leo_comedy_updater/data/data.json", "r", encoding="utf-8") as file:
            json_str = file.read()
            temp_info = json.loads(json_str)

            for participant in temp_info:

                if self.information == None or participant not in self.information:
                    output = "NOVO SHOW!\n " + participant["name"] + " IRA SE APRESENTAR DIA " + participant["date"] + " AS " + participant["time"]
                    try:
                        await send_channel.send(output)
                    except discord.HTTPException as e:
                        print(f"Error sending message: {e}")
                
            for participant in temp_info:

                if participant["days_for_the_show"] == 0:
                    idx = temp_info.index(participant)
                    
                    if self.information == None or participant["days_for_the_show"] != self.information[idx]["days_for_the_show"]:
                        output = "FALTA 1 DIA PARA O EVENTO DO/A " + participant["name"] + " NO DIA " + participant["date"] + " AS " + participant["time"]
                    try:
                        await send_channel.send(output)
                    except discord.HTTPException as e:
                        print(f"Error sending message: {e}")
            
            self.information = temp_info


client = None

async def run_bot():

    intents = discord.Intents.default()
    intents.message_content = True

    global client

    client = MyClient(intents=intents)
    await client.start('Bot-Token-Here')
import os, discord, json
from input_handler import *

if not os.path.exists('data.json'):
    print("Missing data.json file. Terminating")
    quit()
    
file = open('data.json')
data = json.load(file)
file.close()

TOKEN = data['DISCORD_TOKEN']
CHANNEL = data['CHANNEL']
KEYS = data['KEY_CODES']

handler = init_thread()
client = discord.Client()

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

#todo: map messages to key presses and send to queue, 2nd thread to actually activate buttons?
@client.event
async def on_message(message):
    if(message.author != client.user and message.channel.name == CHANNEL):
        if(message.content == "!help"):
            string = "Type any of the following words to press that button in game\n"
            for key in KEYS:
                string = string + key + '\n'
            await message.channel.send(string)
        elif(str.lower(message.content) in KEYS):
            input_queue.put(KEYS[str.lower(message.content)])

print("Press CTRL + Pause/Break to quit the program")
client.run(TOKEN)

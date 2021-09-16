import os, discord, json, queue, time, threading
from pynput.keyboard import Key, Controller

try:
    file = open('data.json')
    data = json.load(file)
    file.close()
    TOKEN = data['DISCORD_TOKEN']
    CHANNEL = data['CHANNEL']
    KEYS = data['KEY_CODES']
    input_queue = queue.Queue()
    keyboard = Controller()
except FileNotFoundError:
    print("Error: data.json file not found")
    exit(1)
except JSONDecodeError:
    print("Error: data is invalid")

client = discord.Client()

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

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

def press(key):
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    time.sleep(0.0001)
    
def handle_inputs():
    while True:
        if not input_queue.empty():
            press(input_queue.get())
            
input_handler_thread = threading.Thread(target=handle_inputs)
input_handler_thread.start()

print("Press CTRL + Pause/Break to quit the program")
client.run(TOKEN)
handler.join()

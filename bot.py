import os, json, queue, time, threading
from discord.ext import commands
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

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if(message.author != bot.user and message.channel.name == CHANNEL):
        if(message.content == "!help"):
            string = "Type any of the following words to press that button in game\n"
            for key in KEYS:
                string = string + key + '\n'
            await message.channel.send(string)
        elif(str.lower(message.content) in KEYS):
            input_queue.put(KEYS[str.lower(message.content)])
    await bot.process_commands(message)

def press(key):
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    time.sleep(0.0001)
    
def handle_inputs(in_queue, run_flag):
    while run_flag.is_set():
        try:
            key = in_queue.get()
            keyboard.press(key)
            time.sleep(0.1)
            keyboard.release(key)
            time.sleep(0.0001)
        except:
            pass            
            
@bot.command()
@commands.is_owner()
async def shutdown(context):
    await context.send("shutting down")
    run_flag.clear()
    input_handler_thread.join()
    await bot.close()

run_flag = threading.Event()
run_flag.set()
input_handler_thread = threading.Thread(target=handle_inputs, args=[input_queue, run_flag])
input_handler_thread.start()

print("Press CTRL + Pause/Break to quit the program")
bot.run(TOKEN)

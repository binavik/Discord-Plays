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
    print("Error: data.json is invalid")
    exit(2)
    
try:
    file = open('banned_users.json')
    BANNED_USERS = json.load(file)
    file.close()
except FileNotFoundError:
    print("Error: banned_users.json file not found")
    exit(3)
except JSONDecodeError:
    print("Error: banned_users.json is invalid")
    exit(4)

run_flag = threading.Event()
run_flag.set()
paused = False

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print("Type !pause to halt input handling.")
    print("Type !resume to resume input handling.")
    

@bot.event
async def on_message(message):
    if(message.author != bot.user and message.channel.name == CHANNEL):
        if message.author.name in BANNED_USERS:
            await message.delete()
        elif(message.content == "!help"):
            string = "Type any of the following words to press that button in game\n"
            for key in KEYS:
                string = string + key + '\n'
            await message.channel.send(string)
        elif not paused:
            try:
                input_queue.put(KEYS[str.lower(message.content)])
            except:
                pass
    await bot.process_commands(message)
    
def handle_inputs(in_queue, flag):
    while flag.is_set():
        try:
            key = in_queue.get()
            keyboard.press(key)
            time.sleep(0.1)
            keyboard.release(key)
            time.sleep(0.0001)
        except:
            pass
    print("exited while loop")
            
@bot.command()
@commands.is_owner()
async def shutdown(context):
    await context.send("shutting down")
    global run_flag, input_handler_thread, bot
    with open('banned_users.json', 'w') as outFile:
        json.dump(BANNED_USERS, outFile, indent=4, sort_keys=True)
    print("clearing run flag")
    run_flag.clear()
    input_queue.put('a')
    input_handler_thread.join()
    await bot.close()

@bot.command()
@commands.is_owner()
async def pause(context):
    global paused
    paused = True
    await context.send("Inputs are now paused, please type !resume to continue.")

@bot.command()
@commands.is_owner()
async def resume(context):
    global paused
    paused = False
    await context.send("You may now resume playing.")

@bot.command()
@commands.is_owner()
async def ban(context, userToBan):
    if userToBan not in BANNED_USERS:
        BANNED_USERS.append(userToBan)
        await context.send(f'{userToBan} added to ban list.') 
    else:
        await context.send(f'Error: {userToBan} already banned.')

@bot.command()
@commands.is_owner()
async def unban(context, userToUnban):
    try:
        BANNED_USERS.remove(userToUnban)
        await context.send(f'{userToUnban} removed from ban list.')
    except:
        await context.send(f'Error {userToUnban} not in banned user list.')
input_handler_thread = threading.Thread(target=handle_inputs, args=[input_queue, run_flag])
input_handler_thread.start()

print("Press CTRL + Pause/Break to quit the program")
try:
    bot.run(TOKEN)
except:
    exit(0)

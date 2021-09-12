# Discord Plays

A Discord bot that takes commands from a specified channel and forwards them as keyboard inputs on the host PC. Inspired by the Twitch Plays Pokemon experiment.

This in theory should be compatible with any game that accepts keyboard input. 

## Dependencies

- discord.py 
- pynput


## Installation
Clone the repository. 
Install [python](https://www.python.org/) for your OS. 
Install the above dependencies.
Follow the directions on Discord's developer portal to [set up a bot](https://discord.com/developers/docs/intro).
Invite the bot to your discord and give it the View Channel, Send Message and Manage Message permissions.
Set the DISCORD_TOKEN variable in data.json to your bot's Token.
Configure the command/key mapping in data.json.

## Running
After setup, simply point a terminal at the folder containing this repository and run:
```
python bot.py
```

## data.json
This file contains the bot token, the name of the text channel you wish to read from and the command to key mapping. 

The KEY_CODES section can be expanded to meet the requirements of any game. Mouse and joystick emulation is currently not supported.
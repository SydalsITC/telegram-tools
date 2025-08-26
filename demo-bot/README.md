
# Demo Telegram Bot
An example for a telegram bot written in python and running in a docker container.

## About
For a small private project, we needed a bot as member in our telegram group that
should create always the same polls if it was asked to. So a bot account was
created using the [telegram botfather](https://telegram.me/BotFather), and some
bot code written in python, using the
[python-telegram-bot](https://python-telegram-bot.org) library.

## How it works
Start the bot with docker compose:
```
docker-compose up # in local directory, or
docker-compose  -f demo-bot/docker-compose.yml up
```
Use the flag "-d" for creating a background process if you like.

The demo-bot directory gets mounted inside the container at /app, making code
and config available. Docker then
- starts entrypoint.sh
- that runs the python code
- which loads the config json file.

## Telegram token
The bot need a telegram token for authentication. The python code awaits this in an 
environment variable called BOTSTELEGRAMTOKEN which is passed through from the outside
by the docker-compose.yml file.

This way works fine for a home setup on a raspberry but is not recommended for production
environments. Make sure to use secrets with docker swarm and kubernetes while adapting
the code respectively.

## Commands

- /about - tells a short story about the bot itself (which ist defined in the config json file).
- /version - shows version of bot.py and the config file
- /hello - just says hello and echoes the name of the calling user
- /userid - shows the numeric user ID of the calling user - which can be used to secure the /polls call just for admins. 
- /polls - creates the polls which are defined in the config file. _This command is restricted._ Make sure your _numeric_ user ID is in the field 'bot.authUsers' in the config file.

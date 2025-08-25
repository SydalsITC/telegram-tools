#!/bin/bash

##
## entrypoint.sh script for telegram bot
##

# external directory with code and config should be mounted here
APPDIR="/app"

# activate python environment with telegram bot modules
. /root/.local/share/pipx/venvs/python-telegram-bot/bin/activate

# start bot
python3 ${APPDIR}/bot.py


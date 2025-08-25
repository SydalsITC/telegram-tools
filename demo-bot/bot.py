##
## sample telegram poll bot
##
## (C) 2025 Sydals IT Consulting - Published under the MIT license
##
## creates predefined polls (cfg.json) if it gets triggered
##

import sys, os, random, re, logging, json
from telegram     import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters
from functools    import wraps

#==== defs ====
BOTVERSION="2025-08-25-2237"
CONFIGFILE="/app/cfg.json"

try:
  BOT_TTOKEN=os.environ["BOTSTELEGRAMTOKEN"]
except:
  print("Env variable BOTSTELEGRAMTOKEN not set; terminating.")
  exit(1)

#---- Basic logging funktion in the file log_file.log
# use 'stream=sys.stdout' or 'filename=LOGFILE'
logging.basicConfig(
  stream=sys.stdout,
  format="%(asctime)s,%(name)s,%(levelname)s,%(message)s",
  level=logging.WARN
)


#==== Restrict access to a handler (decorator) ====
#---- some functions my only be used by authorized
#---- users (defined in cfg.json)
def restricted(func):
  @wraps(func)
  async def wrapped(update, context, *args, **kwargs):
    user_id = update.effective_user.id
    # if user_id not in LIST_OF_ADMINS:
    if user_id not in cfg["bot"]["authUsers"]:
      logging.info(f"403/access denied: {user_id}")
      return
    return await func(update, context, *args, **kwargs)
  return wrapped

#---- this funtion my only be used by authorized users (see decorator above)
@restricted
async def poll_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """
  Sends predefined polls (defined in cfg.json)
  """
  # iterate over polls defined in cfg.json
  for poll_data in cfg["poll_data"]:
    message = await update.effective_message.reply_poll(
      poll_data["question"],
      poll_data["options"],
      is_anonymous = poll_data["anonymous"],
      allows_multiple_answers = poll_data["multipleA"]
    )

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
      message.poll.id: {
        "questions":  poll_data["options"],
        "message_id": message.message_id,
        "chat_id":    update.effective_chat.id,
        "answers":    0
      }
    }
    context.bot_data.update(payload)
  #- end for

  logging.info("polls sent to "  + update.effective_user.first_name )



#==== unrestricted functions ====

#----
async def hello_fn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(f'Hello {update.effective_user.first_name}.')
  logging.info("Said hello to " + update.effective_user.first_name )

#----
async def about_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
    chat_id = update.effective_chat.id,
    message_thread_id = update.effective_message.message_thread_id,
    text    = cfg["bot"]["about"]
  )
  logging.info("about() triggered by "  + update.effective_user.first_name )

#----
async def version_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    message_thread_id = update.effective_message.message_thread_id,
    text="Bot version: " + BOTVERSION + "\nCfg version: " + cfg["configVersion"]
  )
  logging.info("version() triggered by "  + update.effective_user.first_name )


#----
async def userId_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(f'Your numeric telegram user id is {update.effective_user.id}.')
  logging.info("userId() triggered by "  + update.effective_user.first_name )



#==== MAIN ===========================================================

if __name__ == '__main__':
  # load configuration
  try:
    with open(CONFIGFILE) as f:
      cfg = json.load(f)
  except:
    print("Error opening config file '" + CONFIGFILE + "'; terminamting")
    exit(1)

  # Create the Telegram bot application using the provided bot token
  application = ApplicationBuilder().token(BOT_TTOKEN).build()

  # set handlers for specific commands
  application.add_handler(CommandHandler("about",   about_fn  ))
  application.add_handler(CommandHandler("version", version_fn  ))
  application.add_handler(CommandHandler("hello",   hello_fn  ))
  application.add_handler(CommandHandler("userid",  userId_fn ))

  # restricted commands
  application.add_handler(CommandHandler("polls", poll_fn   ))

  logging.warning("Bot is running..." + "\nBot version: " + BOTVERSION + "\nCfg version: " + cfg["configVersion"])
  application.run_polling()


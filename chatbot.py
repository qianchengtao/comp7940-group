from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
from Perplexity import Perplexity
import configparser
import logging

def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token = (config['TELEGRAM']['ACCESS_TOKEN']), use_context = True)
    dispatcher = updater.dispatcher

    # You can set this logging module, so you will know when 
    # and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # dispatcher for perplexity
    global perplexity
    perplexity = Perplexity(config)
    perplexity_handler = MessageHandler(Filters.text & (~Filters.command), equiped_perplexity)
    dispatcher.add_handler(perplexity_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id = update.effective_chat.id, text = reply_message)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('')

def equiped_perplexity(update, context): 
    global perplexity
    reply_message = perplexity.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id = update.effective_chat.id, text = reply_message)

if __name__ == '__main__':
    main()

from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
from Perplexity import Perplexity
#import configparser
import os
import logging
from Firebase import firebase
import requests

def main():
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your bot.")
    # Load your token and create an Updater for your Bot
    #config = configparser.ConfigParser()
    #config.read('config.ini')
    updater = Updater(token = (os.environ['TELEGRAM_ACCESS_TOKEN']), use_context = True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # You can set this logging module, so you will know when 
    # and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    global firebase
    firebase = firebase()

    # dispatcher for perplexity
    global perplexity
    perplexity = Perplexity()
    perplexity_handler = MessageHandler(Filters.text & (~Filters.command), equiped_perplexity)
    dispatcher.add_handler(perplexity_handler)


    dispatcher.add_handler(CommandHandler("send", send))

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

    global firebase
    record = {'question': update.message.text, 'answer': reply_message}
    firebase.submit_data(record)

def send(update, context):
    global firebase
    message = update.message.text
    print(message)
    if 'qct' in message:
        user_data = firebase.get_data('user1')
        print(user_data)
    elif 'clx' in message:
        user_data = firebase.get_data('user2')
        print(user_data)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="The user cannot be found！")
        return

    reply_message = perplexity.submit(message)

    bot_token = user_data[1]
    bot_chatID = str(user_data[0])
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + reply_message
    response = requests.get(send_text)

    context.bot.send_message(chat_id=update.effective_chat.id, text="The message has been sent to "+user_data[2])
    record = {'question': update.message.text, 'answer': reply_message}
    firebase.submit_data(record)

if __name__ == '__main__':
    main()

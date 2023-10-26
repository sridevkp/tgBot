import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

API_KEY = os.get_env('API_KEY')
USERNAME = 'guudMorning_bot'

#commands
async def start_command( update, context ):
    update.message.reply_text("Hello")

async def help_command( update, context ):
    update.message.reply_text("Help is here")


async def custom_command( update, context ):
    update.message.reply_text("custom?")

#respond


async def handle_message( update, context ):
    msg_type = update.message.chat.type #group/private
    text = update.message.text
    response = ''

    if msg_type == "group":
        if USERNAME in text:
            response = "Responding in group"
    else:
        response = "Respondig in private"

    await update.message.reply_text( response )


async def error( update, context ):
    print( update, context)



if __name__ == '__main__' :
    app = Application.builder().token(API_KEY).build()
    #add command handlers
    app.add_handler( CommandHandler( 'start' , start_command ))
    app.add_handler( CommandHandler( 'help'  , start_command ))
    app.add_handler( CommandHandler( 'custom', start_command ))
    #add message handler
    app.add_handler( MessageHandler( filters.TEXT, handle_message ))

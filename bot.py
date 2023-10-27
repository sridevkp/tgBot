import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv('TOKEN')
USERNAME = '@guudMorning_bot'


#commands
async def start_command( update, context ):
    await update.message.reply_text("Hello")

async def help_command( update, context ):
    await update.message.reply_text("Help is here")


async def custom_command( update, context ):
    await update.message.reply_text("custom?")



#respond
async def handle_message( update, context ):
    msg_type = update.message.chat.type #group/private
    text = update.message.text
    response = ''
    
    if msg_type == "group":
        if USERNAME in text:
            response = "Responding in group"
        else:
            return
    else:
        response = "Respondig in private"

    await update.message.reply_text( response )
    await update.message.reply_text( text )


async def error( update, context ):
    print( update, context)



if __name__ == '__main__' :
    app = Application.builder().token(TOKEN).build()
    #add command handlers
    app.add_handler( CommandHandler( 'start' , start_command  ))
    app.add_handler( CommandHandler( 'help'  , help_command   ))
    app.add_handler( CommandHandler( 'custom', custom_command ))
    #add message handler
    app.add_handler( MessageHandler( filters.TEXT, handle_message ))
    #add errr handling 
    app.add_error_handler(error)

    #poll app
    print("polling bot")
    app.run_polling( poll_interval = 3 )

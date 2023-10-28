import os
import requests
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv('TOKEN')
USERNAME = '@guudMorning_bot'

test_audio = open("audio.mp3",'rb')

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

    await update.message.reply_text(response)
    # print(text = update.message.text)

#audio
async def handle_audio_message( update, context ):
    audio = get_file( update.message.voice.get_file().file_path )
    await update.message.reply_audio( audio )



#error handling
async def error( update, context ):
    print("an error occured")
    print( update, context)


def get_file(url, json=False):
    response = requests.get(url)
    if json : return json.loads( response.content )
    return response.content


if __name__ == '__main__' :
    app = Application.builder().token("6774887793:AAEVdb6lBt-fXd5aPYviyt_O7rv_roqEcf8").build()

    #add command handlers
    app.add_handler( CommandHandler( 'start' , start_command  ))
    app.add_handler( CommandHandler( 'help'  , help_command   ))
    app.add_handler( CommandHandler( 'custom', custom_command ))

    #add message handler
    app.add_handler( MessageHandler( filters.TEXT  , handle_message ))        #text
    app.add_handler( MessageHandler( filters.VOICE , handle_audio_message ))  #voice
    app.add_handler( MessageHandler( filters.AUDIO , handle_audio_message ))  #audio

    #add errr handling 
    app.add_error_handler(error)

    #poll app
    print("polling bot")
    app.run_polling( poll_interval = 3 )

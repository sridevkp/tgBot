import os
import requests
import json
import subprocess #runs command in shell/terminal
import speech_recognition as sr
from io import BytesIO
# from pydub import AudioSegment
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
load_dotenv()




TOKEN = os.getenv('TOKEN')
USERNAME = '@guudMorning_bot'

recognizer = sr.Recognizer()

#commands
async def start_command( update, context ):
    URL = "https://thought-of-the-day.p.rapidapi.com/thought"
    headers = {
	    "X-RapidAPI-Key": "7dac8a4a85msh6dc9dbe6114d8bep1e84a2jsn96b16dac4699",
	    "X-RapidAPI-Host": "thought-of-the-day.p.rapidapi.com"
    }

    response = requests.get(URL, headers=headers)

    await update.message.reply_text("Hi")
    await update.message.reply_text('"'+response.json()["data"]+'"')

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
    await update.message.reply_text( "transcribing your audio..." )
    file = await update.message.voice.get_file()
    audio = get_file( file.file_path )
    transcript = "Sorry what?"

    with open("audio.ogg","wb") as file:
        file.write(audio)

    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y']) #convert .ogg file to .wav

    audio_file = sr.AudioFile('audio.wav')

    with audio_file as source:
        try:
            audio = recognizer.record(source)  # listen to file
            transcript = recognizer.recognize_google(audio, language="english") # and write the heard text to a text variable
        except:
            print("somethin went wrnog")


    # await update.message.reply_audio( audio )
    await update.message.reply_text( transcript )



#error handling
async def error( update, context):
    print("an error occured")
    print( update, context )


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
    # app.add_handler( MessageHandler( filters.AUDIO , handle_audio_message ))  #audio

    #add errr handling 
    app.add_error_handler(error)

    #poll app
    print("polling bot")
    app.run_polling( poll_interval = 3 )

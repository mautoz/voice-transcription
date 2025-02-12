#!/usr/bin/env python3
"""
C3PO Voice Transcription

This is a simple Telegram bot script to transcript voice messages.

Install all dependencies and run the script!
"""
import os
from tempfile import TemporaryDirectory
import telegram

import speech_recognition as sr
from pydub import AudioSegment
from telegram.ext import Updater, MessageHandler, Filters

from dotenv import load_dotenv
load_dotenv()

# Replace YOUR_BOT_TOKEN with your Telegram bot token
bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))

def transcribe_audio(update, context):
    """
    The voice message is downloaded in a temporary folder
    and speech recognition transcribes it in chunks.
    """
    with TemporaryDirectory() as temp_path:
        file = context.bot.getFile(update.message.voice.file_id)
        file_name = file.file_path.split("/")[-1]
        file_path = os.path.join(temp_path, file_name)
        file.download(file_path)
        
        # Convert audio if necessary
        file_format = file_name.split(".")[-1]
        if file_format not in ["wav", "aiff", "aif", "aifc", "flac"]:
            sound = AudioSegment.from_file(file_path, format='ogg')
            file_path = os.path.join(temp_path, file_name.split(".")[0] + ".wav")
            sound.export(file_path, format="wav")

        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            # Sometime the script breaks wwith larger audios
            audio_duration = source.DURATION  # Total duration in seconds
            chunk_size = 30  # Process in 30-second chunks
            offset = 0
            full_text = ""

            while offset < audio_duration:
                audio = r.record(source, duration=chunk_size)
                try:
                    text = r.recognize_google(audio, language="pt-BR")
                    full_text += text + " "
                except sr.UnknownValueError:
                    full_text += "[inaudible] "
                except sr.RequestError as err:
                    update.message.reply_text(f"An error occurred: {str(err)}")
                    return
            
                offset += chunk_size  # Move to the next chunk

        update.message.reply_text(full_text.strip())

def main():
    """
    Be careful with your Telegram Token, do not put in your code
    use environment variable.
    """
    updater = Updater(token=os.getenv('TELEGRAM_TOKEN'), use_context=True)
    message_handler = MessageHandler(Filters.voice, transcribe_audio)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

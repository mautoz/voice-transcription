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

TELEGRAM_MAX_LENGTH = 4096
bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))


def transcribe_audio(update, context):
    """
    The voice message is downloaded in a temporary folder
    and speech recognition transcribes it in chunks.
    """
    update.message.reply_text("⏳ Transcrevendo áudio...")

    try:
        with TemporaryDirectory() as temp_path:
            file = context.bot.getFile(update.message.voice.file_id)
            file_name = file.file_path.split("/")[-1]
            file_path = os.path.join(temp_path, file_name)
            file.download(file_path)

            # Convert audio if necessary
            file_format = file_name.split(".")[-1].lower()
            # oga is ogg audio — older ffmpeg doesn't recognize 'oga'
            if file_format == "oga":
                file_format = "ogg"
            if file_format not in ["wav", "aiff", "aif", "aifc", "flac"]:
                sound = AudioSegment.from_file(file_path, format=file_format)
                file_path = os.path.join(temp_path, file_name.split(".")[0] + ".wav")
                sound.export(file_path, format="wav")

            r = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio_duration = source.DURATION
                chunk_size = 30
                offset = 0
                full_text = ""

                while offset < audio_duration:
                    audio = r.record(source, duration=chunk_size)
                    try:
                        text = r.recognize_google(audio, language="pt-BR")
                        full_text += text + " "
                    except sr.UnknownValueError:
                        full_text += "[inaudível] "
                    except sr.RequestError as err:
                        update.message.reply_text(f"❌ Erro na API de reconhecimento: {str(err)}")
                        return

                    offset += chunk_size

        full_text = full_text.strip()
        if not full_text:
            update.message.reply_text("❌ Não foi possível transcrever o áudio.")
            return

        # Split if text exceeds Telegram's message limit
        for i in range(0, len(full_text), TELEGRAM_MAX_LENGTH):
            update.message.reply_text(full_text[i:i + TELEGRAM_MAX_LENGTH])

    except Exception as err:
        update.message.reply_text(f"❌ Erro ao processar o áudio: {str(err)}")


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

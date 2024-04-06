import os
import telegram
from tempfile import TemporaryDirectory
import speech_recognition as sr
from pydub import AudioSegment
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv
load_dotenv()

# Replace YOUR_BOT_TOKEN with your Telegram bot token
bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))

def transcribe_audio(update, context):
    with TemporaryDirectory() as temp_path:
        # Get voice file from Telegram message
        file = context.bot.getFile(update.message.voice.file_id)
        file_name = file.file_path.split("/")[-1]
        file_path = os.path.join(temp_path, file_name)
        file.download(file_path)
        # Check the audio format
        file_format = file_name.split(".")[-1]
        print(file_format)
        if file_format not in ["wav", "aiff", "aif", "aifc", "flac"]:
            sound = AudioSegment.from_file(file_path, format='ogg')            
            file_path = os.path.join(temp_path, file_name.split(".")[0] + ".wav")
            sound.export(file_path, format="wav")

        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio, language="pt-BR")
            update.message.reply_text(text)
        except sr.UnknownValueError:
            update.message.reply_text("It's not Portuguese! Let's try English!")
            try:
                text = text = r.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                update.message.reply_text("I am fluent in over six million forms of communication, but I couldn't understand you! Can you repeat?")
        except sr.RequestError as err:
            update.message.reply_text(f"An error occurred: {str(err)}")

def main():
    updater = Updater(token=os.getenv('TELEGRAM_TOKEN'), use_context=True)
    message_handler = MessageHandler(Filters.voice, transcribe_audio)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
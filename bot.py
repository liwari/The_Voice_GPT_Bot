import telebot
from config import TOKEN, BOT_ADMIN_ID
from log import get_log_file

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Привет! Отправь мне голосовое сообщение или текст, и я тебе отвечу!")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, "Чтобы приступить к общению, отправь мне голосовое сообщение или текст")


@bot.message_handler(commands=['debug'])
def send_logs(message):
    chat_id = message.chat.id
    if chat_id == BOT_ADMIN_ID:
        with get_log_file() as log_file:
            bot.send_document(chat_id, log_file)
    else:
        bot.send_message(chat_id, 'Недостаточно прав для выполнения команды')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, 'Здесь будет текстовый ответ от GPT')


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.send_message(message.from_user.id, ' Здесь будет голосовой ответ от GPT')


@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь следующим сообщением текст, чтобы я его озвучил!')


@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь голосовое сообщение, чтобы я его распознал!')


bot.polling()

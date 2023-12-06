from telebot import TeleBot, types

from src.variables import *
from src.word import get_word

bot = TeleBot('6928817848:AAHcgJVhWSSLnBESjaPdT3vKE4MgMMHgu4Q')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_hello = types.KeyboardButton("Начать")
    bot.send_message(message.from_user.id, hello, reply_markup=markup)
    btn_help = types.KeyboardButton("Помощь")
    bot.send_message(message.from_user.id, help, reply_markup=markup)
    markup.add(btn_hello, btn_help)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, help)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if 'привет' in message.text.lower() or message.text == 'Начать':
        markup = types.InlineKeyboardMarkup()
        btn_start = types.InlineKeyboardButton(start_question, callback_data='yes')
        markup.add(btn_start)
        bot.send_message(message.from_user.id, hello, reply_markup=markup)
    elif message.text == 'Помощь':
        bot.send_message(message.from_user.id, help)
    else:
        bot.send_message(message.from_user.id, error)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        print(get_word())




bot.infinity_polling()

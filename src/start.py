from telebot import TeleBot, types
from os import getenv

from src.variables import *
from src.word import get_meaning, get_word

bot = TeleBot(getenv("BOT_TOKEN"))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton(start_question, callback_data='yes')
    markup.add(btn_start)
    bot.send_message(message.from_user.id, hello, reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, help_)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        global word, word_url, secret_word, hm, tries
        word, word_url = get_word()
        secret_word = '_' * len(word)
        hm = 0
        tries = []
        bot.send_message(call.message.chat.id,
                         hangman[hm] + 'Я загадал слово ' + str(secret_word) + ', попробуй угадать')
    elif call.data == 'meaning':
        markup = types.InlineKeyboardMarkup()
        btn_start = types.InlineKeyboardButton(start_question, callback_data='yes')
        markup.add(btn_start)
        bot.send_message(call.message.chat.id, get_meaning(word_url), reply_markup=markup)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global word, secret_word, hm
    if word:
        sym = message.text.lower()
        if len(sym) == 1 and ord(sym) in range(1072, 1104) and sym not in tries:
            if sym in set(word):
                for i in range(len(word)):
                    if word[i] == sym:
                        secret_word = secret_word[:i] + sym + secret_word[i + 1:]
                bot.send_message(message.from_user.id, right + sym + '!')
                if '_' not in secret_word:
                    markup = types.InlineKeyboardMarkup()
                    btn_m = types.InlineKeyboardButton('Да', callback_data='meaning')
                    markup.add(btn_m)
                    btn_no = types.InlineKeyboardButton('Нет, ' + start_question.lower(), callback_data='yes')
                    markup.add(btn_no)
                    bot.send_message(message.from_user.id, right + 'слово ' + word.capitalize() + '\n' + meaning,
                                     reply_markup=markup)
                    word = ''
            else:
                hm += 1
                bot.send_message(message.from_user.id, wrong)
            tries.append(sym)
            if hm >= 9:
                bot.send_message(message.from_user.id, letters + ', '.join(tries) + '\n' + hangman[hm] + fail + word.capitalize())
                markup = types.InlineKeyboardMarkup()
                btn_m = types.InlineKeyboardButton('Да', callback_data='meaning')
                markup.add(btn_m)
                btn_no = types.InlineKeyboardButton('Нет, ' + start_question.lower(), callback_data='yes')
                markup.add(btn_no)
                bot.send_message(message.from_user.id, meaning, reply_markup=markup)
                word = ''
            elif '_' in secret_word:
                bot.send_message(message.from_user.id,
                                 letters + ', '.join(tries) + '\n' + hangman[hm] + next_1 + secret_word + next_2)
        elif sym in tries:
            bot.send_message(message.from_user.id, sletter)
        else:
            bot.send_message(message.from_user.id, nletter)
    else:
        if 'привет' in message.text.lower() or message.text == 'Начать':
            markup = types.InlineKeyboardMarkup()
            btn_start = types.InlineKeyboardButton(start_question, callback_data='yes')
            markup.add(btn_start)
            bot.send_message(message.from_user.id, hello, reply_markup=markup)
        elif message.text == 'Помощь':
            bot.send_message(message.from_user.id, help_)
        else:
            bot.send_message(message.from_user.id, error)


bot.infinity_polling()

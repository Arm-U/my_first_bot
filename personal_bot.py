import telebot
from config import CONFIG
from RMnewsHandler import RealMadrid
from MIPTnewsHandler import Mipt
import sys

bot = telebot.TeleBot(CONFIG['TOKEN'])
real = RealMadrid()
mipt = Mipt()



@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    text = 'Привет, я личный бот Армана.' \
           '\nЕсли не знаешь что делать напиши /help.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def get_help(message: telebot.types.Message):
    text = 'Это бот который может выдавать последние новости про Реал Мадрид' \
           ' и про МФТИ.\nНапиши "Real Madrid" и получишь новость' \
           ' про Реал Мадрид.\nНапиши "MIPT" и получишь новость про МФТИ.\n' \
           'А если написать сообщение он повторно отправит его' \
           ' и предложить две кнопки: "Real Madrid" и "Mipt".'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message):
    if message.text in ("Real Madrid", "MIPT"):
        if message.text == "Real Madrid":
            date, title, preview, link, image = real.full_news()
        else:
            date, title, preview, link, image = mipt.full_news()
        text = date + '\n' + title + '.\n' + preview + '\n'
        markup = telebot.types.InlineKeyboardMarkup()
        news_link = telebot.types.InlineKeyboardButton(
            text='Ссылка на новость', url=link
        )
        markup.add(news_link)
        bot.send_photo(message.chat.id, image, caption=text, reply_markup=markup)
        return
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_rm = telebot.types.InlineKeyboardButton(text='Real Madrid', callback_data='RM')
    keyboard.add(key_rm)
    key_mipt = telebot.types.InlineKeyboardButton(text='Mipt', callback_data='MIPT')
    keyboard.add(key_mipt)
    bot.send_message(message.chat.id, message.text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: telebot.types.CallbackQuery):
    if call.data == "RM":
        date, title, preview, link, image = real.full_news()
    elif call.data == "MIPT":
        date, title, preview, link, image = mipt.full_news()
    else:
        print("Not such button")
        sys.exit()
    text = date + '\n' + title + '.\n' + preview + '\n'
    markup = telebot.types.InlineKeyboardMarkup()
    news_link = telebot.types.InlineKeyboardButton(
        text='Ссылка на новость', url=link
    )
    markup.add(news_link)
    bot.send_photo(call.message.chat.id, image, caption=text, reply_markup=markup)


bot.polling(none_stop=True)

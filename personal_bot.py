import telebot
from config import CONFIG
from RMnewsHandler import RealMadrid

bot = telebot.TeleBot(CONFIG['TOKEN'])
real = RealMadrid()


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    text = 'Привет, я личный бот Армана.' \
           ' Если не знаешь что делать напиши /help.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def get_help(message: telebot.types.Message):
    text = 'Это бот который может выдавать последние новости про Реал Мадрид' \
           '.\nНапиши "Real Madrid" и получишь новость.' \
           ' А если написать сообщение он повторно отправит его'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message):
    if message.text == 'Real Madrid':
        date, title, preview, link = real.full_news()
        text = date + '\n' + title + '.\n' + preview + '\n'
        markup = telebot.types.InlineKeyboardMarkup()
        news_link = telebot.types.InlineKeyboardButton(
            text='Ссылка на новость', url=link
        )
        markup.add(news_link)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        return
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)

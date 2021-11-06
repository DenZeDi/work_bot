from config import token
import telebot
from telebot import types
import gspread
import time

bot = telebot.TeleBot(token)


class User:
    def __init__(self, chat_id=0, username=''):
        self.chat_id = chat_id
        self.username = username


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, "Привет, меня зовут Хука, я чат-бот кальянной Сквот.")
    time.sleep(1)
    bot.send_message(message.chat.id, "Я помогу тебе забронировать столик у нас и расскажу о новостях.")
    time.sleep(1)
    menu(message)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="О Сквоте", callback_data="squat_button"))
    markup.add(types.InlineKeyboardButton(text="Связаться с сотрудником", callback_data="contact_button"))
    markup.add(types.InlineKeyboardButton(text="Забронировать столик", callback_data="reserve_button"))
    markup.add(types.InlineKeyboardButton(text="Меню", callback_data="menu_button"))

    bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=markup)


def squat(message):
    bot.send_message(message.chat.id, 'Привет, и добро пожаловать в "Сквот"')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = "0"

    if call.data == "squat_button":
        squat(call.message)
    elif call.data == "contact_button":
        answer = 'Напишите @razrabot'
    elif call.data == 'reserve_button':
        answer = 'На какое имя забронировать?'
    elif call.data == 'menu_button':
        answer = 'Меню'

    bot.send_message(call.message.chat.id, answer)


bot.infinity_polling()

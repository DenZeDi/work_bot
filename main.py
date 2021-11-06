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
    menu_markup = types.InlineKeyboardMarkup()
    menu_markup.add(types.InlineKeyboardButton(text="О Сквоте", callback_data="squat_button"))
    menu_markup.add(types.InlineKeyboardButton(text="Связаться с сотрудником", callback_data="contact_button"))
    menu_markup.add(types.InlineKeyboardButton(text="Забронировать столик", callback_data="reserve_button"))
    menu_markup.add(types.InlineKeyboardButton(text="Меню", callback_data="menu_button"))

    bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=menu_markup)


def condition_yes(message):
    bot.send_message(message.chat.id, "yes bla bla")


def condition_no(message):
    bot.send_message(message.chat.id, "bla bla no")


def squat(message):
    condition_markup = types.InlineKeyboardMarkup()
    condition_markup.add(types.InlineKeyboardButton(text="Да", callback_data="cond_yes"))
    condition_markup.add(types.InlineKeyboardButton(text="Нет", callback_data="cond_no"))

    bot.send_message(message.chat.id, 'Привет, и добро пожаловать в "Сквот"')
    time.sleep(1)
    bot.send_message(message.chat.id, "Многие наверное и не знают, что обозначает данное слово, но у него есть своя "
                                      "богатая история, которая берет корни еще с 1950-х годов.")
    time.sleep(1)
    bot.send_message(message.chat.id, "Узнать дальше?", reply_markup=condition_markup)


def contact(message):
    bot.send_message(message.chat.id, "Напишите @razrabot")


def reserve(message):
    bot.send_message(message.chat.id, "На какое имя забронировать?")


def menu_picture(message):
    bot.send_message(message.chat.id, "Меню")


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "squat_button":
        squat(call.message)
    elif call.data == "contact_button":
        contact(call.message)
    elif call.data == 'reserve_button':
        reserve(call.message)
    elif call.data == 'menu_button':
        menu_picture(call.message)
    elif call.data == 'cond_yes':
        condition_yes(call.message)
    elif call.data == 'cond_no':
        condition_no(call.message)


bot.infinity_polling()

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


def next_story(message):
    action_markup = types.InlineKeyboardMarkup()
    action_markup.add(types.InlineKeyboardButton(text="Оставить отзыв", callback_data="feedback"))
    action_markup.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu"))

    bot.send_message(message.chat.id, "Дальше!")
    time.sleep(1)
    bot.send_message(message.chat.id, "Исторически так сложилось, что Сквот - это заброшенное помещение/здание/"
                                      "территория, куда поселились люди, молодые и амбициозные. Они притягивают близких"
                                      " по творческому духу людей и создают различные интересные места, устраивают "
                                      "вечеринки и выставки, к тому же еще и живут там.")
    time.sleep(15)
    bot.send_message(message.chat.id, "У нас конечно же все законно и ничего мы не захватывали. Наш сквоттер оказался "
                                      "любителем рока и хороших вкусных кальянов ;)\n\nМы постарались и создали для вас"
                                      " атмосферу уютного рокерского домика, в который с радостью примем любого, "
                                      "кто захочет стать частью нашей семьи.")
    time.sleep(1)
    bot.send_message(message.chat.id, "Мы ценим открытость и обратную связь, поэтому, если тебе не трудно, "
                                      "оставь нам отзыв) ")
    time.sleep(1)
    bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=action_markup)


# НЕОБХОДИМО НАПИСАТЬ РЕГИСТРАТОР ОТВЕТА!!
def leave_feedback(message):
    bot.send_message(message.chat.id, "Напишите, что о нас думаете!")


def back_to_menu(message):
    menu(message)


def squat(message):
    condition_markup = types.InlineKeyboardMarkup()
    condition_markup.add(types.InlineKeyboardButton(text="Дальше", callback_data="next"))
    condition_markup.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu"))

    bot.send_message(message.chat.id, 'Привет, и добро пожаловать в "Сквот"')
    time.sleep(1)
    bot.send_message(message.chat.id, "Многие наверное и не знают, что обозначает данное слово, но у него есть своя "
                                      "богатая история, которая берет корни еще с 1950-х годов.")
    time.sleep(1)
    bot.send_message(message.chat.id, "Узнать дальше?", reply_markup=condition_markup)


def contact(message):
    back_to_menu_markup = types.InlineKeyboardMarkup()
    back_to_menu_markup.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu"))

    bot.send_message(message.chat.id, "Напишите @razrabot", reply_markup=back_to_menu_markup)


# НЕОБХОДИМО НАПИСАТЬ РЕГИСТРАТОР ОТВЕТА!!
def reserve(message):
    bot.send_message(message.chat.id, "На какое имя забронировать?")


def menu_picture(message):
    bot.send_message(message.chat.id, "Меню")
    bot.send_photo(message.chat.id, photo=open(r"C:\Users\danya\Desktop\Работа\Чат-боты\work_bot\2.jpg", 'rb'))
    bot.send_photo(message.chat.id, photo=open(r"C:\Users\danya\Desktop\Работа\Чат-боты\work_bot\3.jpg", 'rb'))
    bot.send_photo(message.chat.id, photo=open(r"C:\Users\danya\Desktop\Работа\Чат-боты\work_bot\5.jpg", 'rb'))


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
    elif call.data == 'next':
        next_story(call.message)
    elif call.data == 'back_to_menu':
        back_to_menu(call.message)
    elif call.data == 'feedback':
        leave_feedback(call.message)


bot.infinity_polling()

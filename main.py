from config import token
import telebot
from telebot import types
import gspread
import time

bot = telebot.TeleBot(token)

inf = []


class User:
    def __init__(self, chat_id=0, username=''):
        self.chat_id = chat_id
        self.username = username


# Connection to google spreadsheet
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1WmRFckXhQIPeZ7-qKUNKCPgluCg828LwSAc7APsiHRc')
# worksheet = sh.worksheet("Брони сегодня")


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


def get_name_to_reserve(message):
    global inf
    inf = []

    user = User(
        chat_id=message.chat.id,
        username=message.chat.username
    )

    username = user.username
    inf += [username]

    name = bot.send_message(message.chat.id, "На какое имя забронировать?")

    bot.register_next_step_handler(name, get_phone_number, inf)


def get_phone_number(message, inf):
    name = message.text
    inf += [name]

    phone_number = bot.send_message(message.chat.id, "Как с вами связаться? Напишите ваш номер телефона.")

    bot.register_next_step_handler(phone_number, get_date_reserve, inf)


def get_date_reserve(message, inf):
    phone_number = message.text
    inf += [phone_number]

    date_markup = types.InlineKeyboardMarkup()
    date_markup.add(types.InlineKeyboardButton(text="Сегодня", callback_data="сегодня"))
    date_markup.add(types.InlineKeyboardButton(text="Завтра", callback_data="завтра"))

    bot.send_message(message.chat.id, "Когда вы хотите забронировать?", reply_markup=date_markup)


def today_reserve(message, date):
    reserve_day = date
    amount_of_people = bot.send_message(message.chat.id, "На сколько человек?")

    bot.register_next_step_handler(amount_of_people, get_chosen_time, reserve_day)


def tomorrow_reserve(message, date):
    reserve_day = date
    amount_of_people = bot.send_message(message.chat.id, "На сколько человек?")

    bot.register_next_step_handler(amount_of_people, get_chosen_time, reserve_day)


def get_chosen_time(message, reserve_day):
    global inf

    inf += [reserve_day]
    amount_of_people = message.text
    inf += [amount_of_people]

    time_markup = types.InlineKeyboardMarkup()
    time_markup.add(types.InlineKeyboardButton(text="14:00 - 15:30", callback_data="14:00 - 15:30"))
    time_markup.add(types.InlineKeyboardButton(text="15:30 - 17:00", callback_data="15:30 - 17:00"))
    time_markup.add(types.InlineKeyboardButton(text="17:00 - 18:30", callback_data="17:00 - 18:30"))
    time_markup.add(types.InlineKeyboardButton(text="18:30 - 20:00", callback_data="18:30 - 20:00"))
    time_markup.add(types.InlineKeyboardButton(text="20:00 - 21:30", callback_data="20:00 - 21:30"))
    time_markup.add(types.InlineKeyboardButton(text="21:30 - 23:00", callback_data="21:30 - 23:00"))
    time_markup.add(types.InlineKeyboardButton(text="23:00 - 00:00", callback_data="23:00 - 00:00"))

    bot.send_message(message.chat.id, "Выберите время:", reply_markup=time_markup)


def save_reserve_time(message, reserve_time):
    global inf
    inf += [reserve_time]

    back_to_menu_markup = types.InlineKeyboardMarkup()
    back_to_menu_markup.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu"))

    bot.send_message(message.chat.id, "Ваша бронь принята, ждем вас!")
    time.sleep(1)
    bot.send_message(message.chat.id, "Если будут изменения, пожалуйста, предупредите")
    time.sleep(1)
    bot.send_message(message.chat.id, "Вернуться в меню", reply_markup=back_to_menu_markup)


def menu_picture(message):
    bot.send_message(message.chat.id, "Меню")
    bot.send_photo(message.chat.id, photo=open(r"2.jpg", 'rb'))
    bot.send_photo(message.chat.id, photo=open(r"3.jpg", 'rb'))
    bot.send_photo(message.chat.id, photo=open(r"5.jpg", 'rb'))


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "squat_button":
        squat(call.message)
    elif call.data == "contact_button":
        contact(call.message)
    elif call.data == 'reserve_button':
        get_name_to_reserve(call.message)
    elif call.data == 'menu_button':
        menu_picture(call.message)
    elif call.data == 'next':
        next_story(call.message)
    elif call.data == 'back_to_menu':
        back_to_menu(call.message)
    elif call.data == 'feedback':
        leave_feedback(call.message)
    elif call.data == 'сегодня':
        today_reserve(call.message, call.data)
    elif call.data == 'завтра':
        tomorrow_reserve(call.message, call.data)
    elif call.data == '14:00 - 15:30':
        save_reserve_time(call.message, call.data)
    elif call.data == '15:30 - 17:00':
        save_reserve_time(call.message, call.data)
    elif call.data == '17:00 - 18:30':
        save_reserve_time(call.message, call.data)
    elif call.data == '18:30 - 20:00':
        save_reserve_time(call.message, call.data)
    elif call.data == '20:00 - 21:30':
        save_reserve_time(call.message, call.data)
    elif call.data == '21:30 - 23:00':
        save_reserve_time(call.message, call.data)
    elif call.data == '23:00 - 00:00':
        save_reserve_time(call.message, call.data)


bot.infinity_polling()

import time
import telebot
from config import token
from telebot import types
from db import session, Clients, Feedback

bot = telebot.TeleBot(token)

newsletter = ''


class User:
    def __init__(self, chat_id=0, username='', first_name='', phone_number='', reservation_time='',
                 reservation_day='', amount_of_people=''):
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.phone_number = phone_number
        self.reservation_time = reservation_time
        self.reservation_day = reservation_day
        self.amount_of_people = amount_of_people


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


@bot.message_handler(content_types=['text'])
def admin(message):
    if message.text == '1234':
        bot.send_message(message.chat.id, "Добрый день!")
        admin_menu(message)
    else:
        bot.send_message(message.chat.id, "Извините, воспользуйтесь меню.")


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "squat_button":
        squat(call.message)
    elif call.data == "contact_button":
        contact(call.message)
    elif call.data == 'reserve_button':
        get_name_to_reservation(call.message)
    elif call.data == 'menu_button':
        menu_picture(call.message)
    elif call.data == 'next':
        next_story(call.message)
    elif call.data == 'back_to_menu':
        back_to_menu(call.message)
    elif call.data == 'feedback':
        leave_feedback(call.message)
    elif call.data == 'сегодня':
        today_reservation(call.message, call.data)
    elif call.data == 'завтра':
        tomorrow_reservation(call.message, call.data)
    elif call.data == '14:00 - 15:30':
        get_reservation_time(call.message, call.data)
    elif call.data == '15:30 - 17:00':
        get_reservation_time(call.message, call.data)
    elif call.data == '17:00 - 18:30':
        get_reservation_time(call.message, call.data)
    elif call.data == '18:30 - 20:00':
        get_reservation_time(call.message, call.data)
    elif call.data == '20:00 - 21:30':
        get_reservation_time(call.message, call.data)
    elif call.data == '21:30 - 23:00':
        get_reservation_time(call.message, call.data)
    elif call.data == '23:00 - 00:00':
        get_reservation_time(call.message, call.data)
    elif call.data == 'view_reservation':
        view_reservation(call.message)
    elif call.data == 'make_a_newsletter':
        make_a_newsletter(call.message)
    elif call.data == 'send_newsletter':
        send_newsletter(call.message)
    elif call.data == 'cancel_sending':
        admin_menu(call.message)
    elif call.data == 'back_to_admin_menu':
        admin_menu(call.message)


def admin_menu(message):
    choose_markup = types.InlineKeyboardMarkup()
    choose_markup.add(types.InlineKeyboardButton(text='Посмотреть брони', callback_data='view_reservation'))
    choose_markup.add(types.InlineKeyboardButton(text='Сделать рассылку', callback_data='make_a_newsletter'))

    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=choose_markup)


def view_reservation(message):
    url = 'https://docs.google.com/spreadsheets/d/1WmRFckXhQIPeZ7-qKUNKCPgluCg828LwSAc7APsiHRc/edit?usp=sharing'

    url_markup = types.InlineKeyboardMarkup()
    url_markup.add(types.InlineKeyboardButton(text='Брони', url=url))

    back_to_menu_markup = types.InlineKeyboardMarkup()
    back_to_menu_markup.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_admin_menu"))

    # Запрос брони из базы данных
    result = session.query(Clients).filter(Clients.reservation_day == 'сегодня').\
        order_by(Clients.reservation_time.asc())

    bot.send_message(message.chat.id, "Сегодня есть брони на: \nимя | номер телефона | время")
    for row in result:
        bot.send_message(message.chat.id, f"{row.client_name} | {row.phone_number} | {row.reservation_time}")

    time.sleep(2)
    bot.send_message(message.chat.id, "Посмотреть подобнее в гугл таблицах", reply_markup=url_markup)
    time.sleep(2)
    bot.send_message(message.chat.id, "Вернуться в меню", reply_markup=back_to_menu_markup)


def make_a_newsletter(message):
    newsletter = bot.send_message(message.chat.id, "Напишите сообщение, которое хотите всем отправить")
    bot.register_next_step_handler(newsletter, sure_to_send)


def sure_to_send(message):
    global newsletter
    newsletter = message.text

    sure_markup = types.InlineKeyboardMarkup()
    sure_markup.add(types.InlineKeyboardButton(text='Да', callback_data='send_newsletter'))
    sure_markup.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancel_sending'))

    bot.send_message(message.chat.id, "Точно отправляем?", reply_markup=sure_markup)


def send_newsletter(message):
    result = session.query(Clients.client_chat_id).distinct()
    for row in result:
        bot.send_message(row[0], f"{newsletter}")

    bot.send_message(message.chat.id, "Рассылка отправлена!")
    admin_menu(message)


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
    time.sleep(1)
    bot.send_message(message.chat.id, "У нас конечно же все законно и ничего мы не захватывали. Наш сквоттер оказался "
                                      "любителем рока и хороших вкусных кальянов ;)\n\nМы постарались и создали для вас"
                                      " атмосферу уютного рокерского домика, в который с радостью примем любого, "
                                      "кто захочет стать частью нашей семьи.")
    time.sleep(1)
    bot.send_message(message.chat.id, "Мы ценим открытость и обратную связь, поэтому, если тебе не трудно, "
                                      "оставь нам отзыв) ")
    time.sleep(1)
    bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=action_markup)


def leave_feedback(message):
    feedback_to_db = bot.send_message(message.chat.id, "Напишите, что о нас думаете!")
    bot.register_next_step_handler(feedback_to_db, feedback_thanks)


def feedback_thanks(message):
    feedback_to_db = message.text

    user = User(
        chat_id=message.chat.id,
        username=message.chat.username,
        first_name=message.chat.first_name
    )

    session.add(Feedback(client_username=user.username, client_name=user.first_name, feedback=feedback_to_db))
    session.commit()

    back_to_menu_markup = types.InlineKeyboardMarkup()
    back_to_menu_markup.add(types.InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu"))

    bot.send_message(message.chat.id, "Спасибо за отзыв!", reply_markup=back_to_menu_markup)


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


def get_client_id():
    row = session.query(Clients.client_id).all()
    return row[len(row) - 1][0]


def get_name_to_reservation(message):
    user = User(
        chat_id=message.chat.id,
        username=message.chat.username,
    )

    chat_id = user.chat_id
    username = user.username

    session.add(Clients(client_chat_id=chat_id, client_username=username))

    name = bot.send_message(message.chat.id, "На какое имя забронировать?")

    bot.register_next_step_handler(name, get_phone_number)


def get_phone_number(message):
    name = message.text
    row = get_client_id()

    session.query(Clients).filter(Clients.client_id == row).\
        update({Clients.client_name: name}, synchronize_session=False)

    phone_number = bot.send_message(message.chat.id, "Как с вами связаться? Напишите ваш номер телефона.")

    bot.register_next_step_handler(phone_number, get_date_reservation)


def get_date_reservation(message):
    phone_number = message.text
    row = get_client_id()

    session.query(Clients).filter(Clients.client_id == row).\
        update({Clients.phone_number: phone_number}, synchronize_session=False)

    date_markup = types.InlineKeyboardMarkup()
    date_markup.add(types.InlineKeyboardButton(text="Сегодня", callback_data="сегодня"))
    date_markup.add(types.InlineKeyboardButton(text="Завтра", callback_data="завтра"))

    bot.send_message(message.chat.id, "Когда вы хотите забронировать?", reply_markup=date_markup)


def today_reservation(message, date):
    reservation_day = date
    amount_of_people = bot.send_message(message.chat.id, "На сколько человек?")

    bot.register_next_step_handler(amount_of_people, get_chosen_time, reservation_day)


def tomorrow_reservation(message, date):
    reservation_day = date
    amount_of_people = bot.send_message(message.chat.id, "На сколько человек?")

    bot.register_next_step_handler(amount_of_people, get_chosen_time, reservation_day)


def get_chosen_time(message, reserve_day):
    amount_of_people = message.text
    row = get_client_id()

    session.query(Clients).filter(Clients.client_id == row).\
        update({Clients.amount_of_people: amount_of_people, Clients.reservation_day: reserve_day},
               synchronize_session=False)

    time_markup = types.InlineKeyboardMarkup()
    time_markup.add(types.InlineKeyboardButton(text="14:00 - 15:30", callback_data="14:00 - 15:30"))
    time_markup.add(types.InlineKeyboardButton(text="15:30 - 17:00", callback_data="15:30 - 17:00"))
    time_markup.add(types.InlineKeyboardButton(text="17:00 - 18:30", callback_data="17:00 - 18:30"))
    time_markup.add(types.InlineKeyboardButton(text="18:30 - 20:00", callback_data="18:30 - 20:00"))
    time_markup.add(types.InlineKeyboardButton(text="20:00 - 21:30", callback_data="20:00 - 21:30"))
    time_markup.add(types.InlineKeyboardButton(text="21:30 - 23:00", callback_data="21:30 - 23:00"))
    time_markup.add(types.InlineKeyboardButton(text="23:00 - 00:00", callback_data="23:00 - 00:00"))

    bot.send_message(message.chat.id, "Выберите время:", reply_markup=time_markup)


def get_reservation_time(message, reservation_time):
    row = get_client_id()

    session.query(Clients).filter(Clients.client_id == row).\
        update({Clients.reservation_time: reservation_time}, synchronize_session=False)
    session.commit()

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
    back_to_menu(message)


bot.infinity_polling()

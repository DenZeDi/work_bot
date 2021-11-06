from config import token
import telebot

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message, "Привет, меня зовут Хука, я чат-бот кальянной Сквот.")


bot.polling(True)

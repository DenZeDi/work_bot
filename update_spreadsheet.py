import time
import gspread
import schedule
from db import engine, clients, feedback

# Connection to google spreadsheet
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1WmRFckXhQIPeZ7-qKUNKCPgluCg828LwSAc7APsiHRc')

conn = engine.connect()


def update_reservation_today():
    s = clients.select().where(clients.c.reservation_day == 'сегодня').order_by(clients.c.reservation_time.asc())
    result = conn.execute(s)
    row = result.fetchall()

    worksheet_today = sh.worksheet("Брони сегодня")
    worksheet_today.batch_clear(["A2:D60"])

    for index in range(len(row)):
        username = row[index][1]
        name = row[index][2]
        phone_number = row[index][3]
        reservation_time = row[index][4]

        # Обновлять гугл таблицу с сегодняшними бронями
        worksheet_today.update(f'A{index + 2}', username)
        worksheet_today.update(f'B{index + 2}', name)
        worksheet_today.update(f'C{index + 2}', phone_number)
        worksheet_today.update(f'D{index + 2}', reservation_time)


def update_reservation_tomorrow():
    s = clients.select().where(clients.c.reservation_day == 'завтра').order_by(clients.c.reservation_time.asc())
    result = conn.execute(s)
    row = result.fetchall()

    worksheet_tomorrow = sh.worksheet("Брони завтра")
    worksheet_tomorrow.batch_clear(["A2:D60"])

    for index in range(len(row)):
        username = row[index][1]
        name = row[index][2]
        phone_number = row[index][3]
        reservation_time = row[index][4]

        # Обновлять гугл таблицу с завтрашними бронями
        worksheet_tomorrow.update(f'A{index + 2}', username)
        worksheet_tomorrow.update(f'B{index + 2}', name)
        worksheet_tomorrow.update(f'C{index + 2}', phone_number)
        worksheet_tomorrow.update(f'D{index + 2}', reservation_time)


def update_feedback():
    s = feedback.select()
    result = conn.execute(s)
    row = result.fetchall()

    for index in range(len(row)):
        username = row[index][1]
        name = row[index][2]
        fb = row[index][3]

        # Обновлять гугл таблицу с отзывами
        worksheet_feedback = sh.worksheet("Отзывы")
        worksheet_feedback.update(f'A{index + 2}', username)
        worksheet_feedback.update(f'B{index + 2}', name)
        worksheet_feedback.update(f'C{index + 2}', fb)


schedule.every().minutes.do(update_reservation_today)
schedule.every().minute.do(update_reservation_tomorrow)
schedule.every().minute.do(update_feedback)

while True:
    schedule.run_pending()
    time.sleep(1)

import time
import gspread
import schedule
from db import Clients, Feedback, session

# Connection to google spreadsheet
gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1WmRFckXhQIPeZ7-qKUNKCPgluCg828LwSAc7APsiHRc')


def update_reservation_today():
    result = session.query(Clients).filter(Clients.reservation_day == 'сегодня').\
        order_by(Clients.reservation_time).all()

    worksheet_today = sh.worksheet("Брони сегодня")
    worksheet_today.batch_clear(["A2:D60"])

    index = 0
    for row in result:
        username = row.client_username
        name = row.client_name
        phone_number = row.phone_number
        reservation_time = row.reservation_time

        # Обновлять гугл таблицу с сегодняшними бронями
        worksheet_today.update(f'A{index + 2}', username)
        worksheet_today.update(f'B{index + 2}', name)
        worksheet_today.update(f'C{index + 2}', phone_number)
        worksheet_today.update(f'D{index + 2}', reservation_time)

        index += 1


def update_reservation_tomorrow():
    result = session.query(Clients).filter(Clients.reservation_day == 'завтра'). \
        order_by(Clients.reservation_time).all()

    worksheet_tomorrow = sh.worksheet("Брони завтра")
    worksheet_tomorrow.batch_clear(["A2:D60"])

    index = 0
    for row in result:
        username = row.client_username
        name = row.client_name
        phone_number = row.phone_number
        reservation_time = row.reservation_time

        # Обновлять гугл таблицу с завтрашними бронями
        worksheet_tomorrow.update(f'A{index + 2}', username)
        worksheet_tomorrow.update(f'B{index + 2}', name)
        worksheet_tomorrow.update(f'C{index + 2}', phone_number)
        worksheet_tomorrow.update(f'D{index + 2}', reservation_time)

        index += 1


def update_feedback():
    result = session.query(Feedback).all()

    worksheet_feedback = sh.worksheet("Отзывы")
    worksheet_feedback.batch_clear(["A2:C150"])

    index = 0
    for row in result:
        username = row.client_username
        name = row.client_name
        fb = row.feedback

        # Обновлять гугл таблицу с отзывами
        worksheet_feedback.update(f'A{index + 2}', username)
        worksheet_feedback.update(f'B{index + 2}', name)
        worksheet_feedback.update(f'C{index + 2}', fb)

        index += 1


schedule.every().minutes.do(update_reservation_today)
schedule.every().minute.do(update_reservation_tomorrow)
schedule.every().minute.do(update_feedback)

while True:
    schedule.run_pending()
    time.sleep(1)

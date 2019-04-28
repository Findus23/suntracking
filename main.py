import time
from datetime import timedelta, datetime

import schedule
import telegram

import guess
from config import telegram_token, telegram_chat_id


def timedelta_to_string(delta: timedelta):
    minutes, seconds = divmod(delta.seconds, 60)
    return ":".join(map(str, [minutes, seconds]))


def send_notification(time, accuracy, future=False):
    subject = "☀️ at {time} (±{acc})".format(time=time.strftime("%H:%M:%S"), acc=timedelta_to_string(accuracy))
    if future:
        subject += " - 10 minutes left"
    bot = telegram.Bot(token=telegram_token)

    bot.sendMessage(chat_id=telegram_chat_id, text=subject)
    # sendmail(subject, subject)
    return schedule.CancelJob


def create_schedule():
    with open("average.txt") as file:
        lines = file.readlines()
        altitude = float(lines[0].strip())
        standard_derivation = float(lines[1].strip())
    print(altitude, standard_derivation)

    sunset = guess.get_time(altitude)
    accuracy = guess.get_time(altitude - standard_derivation) - sunset
    print(accuracy)
    print(sunset)
    s = schedule.every().day
    s.at_time = sunset.time()
    s.do(send_notification, sunset, accuracy)

    p = schedule.every().day
    p.at_time = (sunset - timedelta(minutes=10)).time()
    p.do(send_notification, sunset, accuracy, True)


create_schedule()

schedule.every().day.at("12:00").do(create_schedule)
if datetime.now().hour > 12:
    create_schedule()

while True:
    schedule.run_pending()
    time.sleep(1)

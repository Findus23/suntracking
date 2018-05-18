import time

import schedule

import guess
from sendmail import sendmail


def send_notification(time, future=False):
    subject = "☀️ at {time}".format(time=time)
    if future:
        subject += " - {min} minutes left".format(min=future)
    sendmail(subject, subject)
    return schedule.CancelJob


def create_schedule():
    with open("average.txt") as file:
        lines = file.readlines()
        altitude = float(lines[0].strip())
        standard_derivation = float(lines[1].strip())
    print(altitude, standard_derivation)

    sunset_time = guess.get_time(altitude).time()

    s = schedule.every().day
    s.at_time = sunset_time
    s.do(send_notification, sunset_time)

    prewarn_time = guess.get_time(altitude + standard_derivation * 3).time()
    s = schedule.every().day
    print(prewarn_time)
    s.at_time = prewarn_time
    s.do(send_notification, sunset_time, future=prewarn_time - sunset_time)


create_schedule()

schedule.every().day.at("12:00").do(create_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)

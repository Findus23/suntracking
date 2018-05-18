import time

import schedule

import guess


def send_notification(on_time=False):
    print("DAS IST EIN TEST")
    return schedule.CancelJob


def create_schedule():
    with open("average.txt") as file:
        lines = file.readlines()
        altitude = float(lines[0].strip())
        standard_derivation = float(lines[1].strip())
    print(altitude, standard_derivation)

    s = schedule.every().day

    s.at_time = guess.get_time(altitude).time()
    s.at_time = guess.get_time(altitude).time()
    s.do(send_notification, on_time=True)

    s = schedule.every().day
    print(guess.get_time(altitude + standard_derivation * 3).time())
    s.at_time = guess.get_time(altitude + standard_derivation * 3).time()
    s.do(send_notification)


create_schedule()

schedule.every().day.at("12:00").do(create_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)

import random
import string
import time


def fake_name():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(3, 7))).capitalize()


def strTimeProp(start, end, format):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + random.random() * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end):
    return strTimeProp(start, end, '%d/%m/%Y')


def generate_players(number_of_players):

    return [{"first_name": fake_name(), "last_name": fake_name(), "birth_date": randomDate("1/1/1958", "1/1/2005"),
             "sex": ["Male", "Female"][random.randint(0, 1)], "rank": random.randint(800, 1800)}
            for i in range(number_of_players)]

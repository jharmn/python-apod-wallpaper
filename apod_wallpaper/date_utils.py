from datetime import date, datetime, timedelta
from random import randint

def format_date(d):
    return d.strftime("%Y-%m-%d")

def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def random_date(start, end):
    year = randint(start.year, end.year)
    month = randint(start.month, end.month)
    day = randint(start.day, end.day)
    return date(year, month, day)

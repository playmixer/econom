from datetime import datetime, timedelta
from flask import request
from calendar import monthrange


def selected_month():
    month = request.args.get('month')
    year = request.args.get('year')

    if month is not year is not None:
        month = int(month)
        year = int(year)

    if month is year is None:
        date_now = datetime.now()
        month = date_now.month
        year = date_now.year

    return month, year


def max_min_datetime_in_month(month, year):
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    d1 = datetime(year, month, 1)
    d2 = datetime(year, month, monthrange(year, month)[1])
    return d1, d2


def prev_month(month, year):
    month -= 1
    if not month:
        year -= 1
        month = 12
    return month, year


def next_month(month, year):
    month += 1
    if month > 12:
        year += 1
        month = 1
    return month, year


def name_of_month(month):
    names = ["Январь", "Феврлаль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
             "Декабрь"]

    return names[month - 1]

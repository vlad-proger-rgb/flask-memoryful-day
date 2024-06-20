import calendar
from datetime import datetime, timedelta

def get_days_in_month(year: int, month: int):
    return calendar.monthrange(year, month)[1]

def month_number_to_name(month_number):
    if 1 <= month_number <= 12:
        month_name = calendar.month_name[month_number]
        return month_name
    else:
        return "Invalid month number"

def get_current_year():
    return datetime.now().year

def date_to_timestamp(year, month, day):
    date_obj = datetime(year, month, day)

    timestamp = int(date_obj.timestamp())

    return timestamp

def timestamp_to_date(timestamp):
    date_obj = datetime.fromtimestamp(timestamp)

    year = date_obj.year
    month = date_obj.month
    day = date_obj.day

    return year, month, day

def get_date_one_month_ago(date = None):
    return (date if date else datetime.now()) - timedelta(30)

def get_today():
    return datetime.now()
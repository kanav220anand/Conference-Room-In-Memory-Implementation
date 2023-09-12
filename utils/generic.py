from datetime import date, datetime, timedelta


def get_today():
    return date.today().strftime("%d-%m-%Y")


def get_month_year():
    return date.today().strftime("%m-%Y")


def get_date_before(days=30):
    return (date.today()-timedelta(days=30)).strftime("%d-%m-%Y")


def get_current_hour_minute():
    return datetime.now().strftime('%H:%M')


# def compare_dates_string(date_str1, date_str2):
#     return datetime.strptime(date_str1, '%m-%d-%Y') >= \
#         datetime.strptime(date_str2, '%m-%d-%Y')


def check_if_dates_are_same(date_str1, date_str2):
    return datetime.strptime(date_str1, '%d-%m-%Y') == \
        datetime.strptime(date_str2, '%d-%m-%Y')


def get_time_difference_in_minutes(time1, time2):
    t1 = datetime.strptime(time1, '%H:%M')
    t2 = datetime.strptime(time2, '%H:%M')
    td = t2 - t1
    return abs(td.total_seconds()/60)


def find_if_date_in_range(date, range):
    if len(range) != 2:
        raise Exception("Invalid date range input")

    start = datetime.strptime(range[0], '%d-%m-%Y')
    end = datetime.strptime(range[1], '%d-%m-%Y')
    dtc = datetime.strptime(date, '%d-%m-%Y')

    if dtc >= start and dtc <= end:
        return True
    return False
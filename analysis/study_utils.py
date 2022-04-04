from dateutil import relativedelta


def last_day_of_month(dt):
    return dt + relativedelta.relativedelta(day=31)


def last_day_of_week(dt):
    return dt + relativedelta.relativedelta(day=7)

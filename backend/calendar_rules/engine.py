from datetime import timedelta, timezone
from zoneinfo import ZoneInfo


def add_business_hours(start, hours, country):
    local_tz = ZoneInfo(country.timezone)
    current = start.astimezone(local_tz)
    remaining = timedelta(hours=hours)
    working_days = country.working_day_numbers()
    holidays = set(country.holidays.values_list("date", flat=True))

    while remaining > timedelta(0):
        if not is_working_day(current, working_days, holidays):
            current = next_day_start(current, country)
            continue

        day_start = at_time(current, country.workday_start)
        day_end = at_time(current, country.workday_end)

        if current < day_start:
            current = day_start
        if current >= day_end:
            current = next_day_start(current, country)
            continue

        available = day_end - current
        if remaining <= available:
            current = current + remaining
            remaining = timedelta(0)
        else:
            remaining = remaining - available
            current = next_day_start(current, country)

    return current.astimezone(timezone.utc)


def is_working_day(moment, working_days, holidays):
    if moment.weekday() not in working_days:
        return False
    if moment.date() in holidays:
        return False
    return True


def at_time(moment, clock):
    return moment.replace(hour=clock.hour, minute=clock.minute, second=0, microsecond=0)


def next_day_start(moment, country):
    next_day = moment + timedelta(days=1)
    return at_time(next_day, country.workday_start)

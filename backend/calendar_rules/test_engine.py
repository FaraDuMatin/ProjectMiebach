from datetime import date

from conftest import local

from .engine import add_business_hours
from .models import Holiday

TORONTO = "America/Toronto"
BERLIN = "Europe/Berlin"


def test_inside_working_hours(canada):
    start = local(2026, 9, 14, 10, TORONTO)
    assert add_business_hours(start, 2, canada) == local(2026, 9, 14, 12, TORONTO)


def test_crosses_the_night(canada):
    start = local(2026, 9, 14, 16, TORONTO)
    assert add_business_hours(start, 2, canada) == local(2026, 9, 15, 10, TORONTO)


def test_skips_the_weekend(canada):
    start = local(2026, 9, 18, 16, TORONTO)
    assert add_business_hours(start, 2, canada) == local(2026, 9, 21, 10, TORONTO)


def test_skips_a_holiday(canada):
    Holiday.objects.create(country=canada, date=date(2026, 9, 15), name="Test day")
    start = local(2026, 9, 14, 16, TORONTO)
    assert add_business_hours(start, 2, canada) == local(2026, 9, 16, 10, TORONTO)


def test_two_countries_same_start_different_due(canada, germany):
    start = local(2026, 9, 14, 14, "UTC")
    due_canada = add_business_hours(start, 4, canada)
    due_germany = add_business_hours(start, 4, germany)
    assert due_canada == local(2026, 9, 14, 14, TORONTO)
    assert due_germany == local(2026, 9, 15, 11, BERLIN)
    assert due_canada != due_germany


def test_zero_hours_returns_start(canada):
    start = local(2026, 9, 14, 10, TORONTO)
    assert add_business_hours(start, 0, canada) == start

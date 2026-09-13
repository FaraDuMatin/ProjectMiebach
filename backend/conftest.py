from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest

from calendar_rules.models import Country


def local(year, month, day, hour, tz):
    return datetime(year, month, day, hour, tzinfo=ZoneInfo(tz))


@pytest.fixture
def canada(db):
    return Country.objects.create(
        code="CA",
        name="Canada",
        timezone="America/Toronto",
        workday_start=time(9),
        workday_end=time(17),
        working_days="0,1,2,3,4",
    )


@pytest.fixture
def germany(db):
    return Country.objects.create(
        code="DE",
        name="Germany",
        timezone="Europe/Berlin",
        workday_start=time(8),
        workday_end=time(17),
        working_days="0,1,2,3,4",
    )


@pytest.fixture
def api(client, django_user_model):
    user = django_user_model.objects.create_user(username="tester", password="secret123")
    client.force_login(user)
    return client

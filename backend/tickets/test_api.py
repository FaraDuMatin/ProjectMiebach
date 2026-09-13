from datetime import timedelta

from django.utils import timezone

from .models import Ticket


def make_ticket(country, key, created_at, due_at):
    return Ticket.objects.create(
        jira_key=key,
        title=key,
        priority="P2",
        status="To Do",
        country=country,
        created_at=created_at,
        due_at=due_at,
    )


def test_tickets_require_login(client, canada):
    assert client.get("/api/tickets/").status_code == 403


def test_tickets_filtered_by_bucket(api, canada):
    now = timezone.now()
    make_ticket(canada, "OPS-1", now - timedelta(hours=8), now - timedelta(hours=1))
    make_ticket(canada, "OPS-2", now, now + timedelta(hours=8))
    response = api.get("/api/tickets/?bucket=breached")
    keys = []
    for ticket in response.json():
        keys.append(ticket["jira_key"])
    assert keys == ["OPS-1"]


def test_stats_shape(api, canada, germany):
    now = timezone.now()
    make_ticket(canada, "OPS-1", now, now + timedelta(hours=8))
    make_ticket(canada, "OPS-2", now, now + timedelta(hours=8))
    make_ticket(germany, "OPS-3", now - timedelta(hours=8), now - timedelta(hours=1))
    data = api.get("/api/stats/").json()
    assert data["by_country"] == {"CA": 2, "DE": 1}
    assert data["by_bucket"] == {"at_risk": 0, "on_time": 2, "breached": 1, "paused": 0}

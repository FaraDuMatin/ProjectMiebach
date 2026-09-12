from conftest import local

from calendar_rules.models import SlaPolicy

from .models import PAUSED_STATUS, ClockEvent, Ticket
from .sla import bucket, recompute

TORONTO = "America/Toronto"


def make_ticket(country, created_at, status="In Progress"):
    SlaPolicy.objects.get_or_create(country=country, priority="P1", defaults={"hours": 4})
    return Ticket.objects.create(
        jira_key="OPS-1",
        title="Test",
        priority="P1",
        status=status,
        country=country,
        created_at=created_at,
    )


def test_recompute_without_pause(canada):
    ticket = make_ticket(canada, local(2026, 9, 14, 10, TORONTO))
    recompute(ticket)
    assert ticket.paused_minutes == 0
    assert ticket.due_at == local(2026, 9, 14, 14, TORONTO)


def test_recompute_with_one_pause(canada):
    ticket = make_ticket(canada, local(2026, 9, 14, 10, TORONTO))
    ClockEvent.objects.create(ticket=ticket, status_from="In Progress", status_to=PAUSED_STATUS, at=local(2026, 9, 14, 11, TORONTO))
    ClockEvent.objects.create(ticket=ticket, status_from=PAUSED_STATUS, status_to="In Progress", at=local(2026, 9, 14, 12, TORONTO))
    recompute(ticket)
    assert ticket.paused_minutes == 60
    assert ticket.due_at == local(2026, 9, 14, 15, TORONTO)


def test_old_ticket_is_breached(canada):
    ticket = make_ticket(canada, local(2026, 1, 5, 10, TORONTO))
    recompute(ticket)
    assert bucket(ticket) == "breached"

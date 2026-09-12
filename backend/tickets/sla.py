from datetime import timedelta

from django.utils import timezone

from calendar_rules.engine import add_business_hours
from calendar_rules.models import SlaPolicy

from .models import PAUSED_STATUS

AT_RISK_FRACTION = 0.2


def paused_minutes(ticket):
    total = timedelta(0)
    paused_since = None
    for event in ticket.clock_events.all():
        if event.status_to == PAUSED_STATUS:
            paused_since = event.at
        elif paused_since is not None:
            total = total + (event.at - paused_since)
            paused_since = None
    if paused_since is not None:
        total = total + (timezone.now() - paused_since)
    return int(total.total_seconds() / 60)


def recompute(ticket):
    policy = SlaPolicy.objects.get(country=ticket.country, priority=ticket.priority)
    ticket.paused_minutes = paused_minutes(ticket)
    due = add_business_hours(ticket.created_at, policy.hours, ticket.country)
    ticket.due_at = due + timedelta(minutes=ticket.paused_minutes)
    ticket.save()
    return ticket


def bucket(ticket):
    if ticket.status == PAUSED_STATUS:
        return "paused"
    now = timezone.now()
    if ticket.due_at < now:
        return "breached"
    total = ticket.due_at - ticket.created_at
    left = ticket.due_at - now
    if left < total * AT_RISK_FRACTION:
        return "at_risk"
    return "on_time"

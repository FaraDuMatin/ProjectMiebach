from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from calendar_rules.models import Country
from tickets.models import ClockEvent, Ticket
from tickets.sla import recompute

PRIORITY_MAP = {
    "Highest": "P1",
    "High": "P2",
    "Medium": "P3",
    "Low": "P4",
    "Lowest": "P4",
}


def upsert_ticket(issue):
    fields = issue["fields"]
    country_value = fields.get(settings.JIRA_COUNTRY_FIELD)
    if country_value is None:
        return None

    ticket = Ticket.objects.filter(jira_key=issue["key"]).first()
    if ticket is None:
        ticket = Ticket(jira_key=issue["key"])

    new_status = fields["status"]["name"]
    if ticket.pk and ticket.status != new_status:
        ClockEvent.objects.create(ticket=ticket, status_from=ticket.status, status_to=new_status, at=timezone.now())

    ticket.title = fields["summary"]
    ticket.priority = PRIORITY_MAP[fields["priority"]["name"]]
    ticket.status = new_status
    ticket.country = Country.objects.get(code=country_value["value"])
    ticket.created_at = parse_datetime(fields["created"])
    ticket.last_synced_at = timezone.now()
    ticket.save()
    return ticket


def sync_issue(client, issue):
    ticket = upsert_ticket(issue)
    if ticket is None:
        return None
    recompute(ticket)
    due_date = ticket.due_at.date()
    if issue["fields"].get("duedate") != due_date.isoformat():
        client.set_due_date(ticket.jira_key, due_date)
    return ticket

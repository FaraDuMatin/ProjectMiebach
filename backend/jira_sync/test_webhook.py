from conftest import local

from calendar_rules.models import SlaPolicy
from tickets.models import Ticket

from .client import JiraClient

COUNTRY_FIELD = "customfield_10041"


def payload():
    return {
        "webhookEvent": "jira:issue_created",
        "issue": {
            "key": "OPS-9",
            "fields": {
                "summary": "Webhook test",
                "status": {"name": "To Do"},
                "priority": {"name": "Highest"},
                "created": "2026-09-14T10:00:00.000-0400",
                "duedate": None,
                COUNTRY_FIELD: {"value": "CA"},
            },
        },
    }


def fake_set_due_date(self, key, date):
    pass


def test_webhook_without_secret_is_403(client, settings):
    settings.JIRA_WEBHOOK_SECRET = "test-secret"
    response = client.post("/api/jira/webhook/", payload(), content_type="application/json")
    assert response.status_code == 403


def test_webhook_creates_ticket(client, settings, canada, monkeypatch):
    settings.JIRA_WEBHOOK_SECRET = "test-secret"
    settings.JIRA_COUNTRY_FIELD = COUNTRY_FIELD
    SlaPolicy.objects.create(country=canada, priority="P1", hours=4)
    monkeypatch.setattr(JiraClient, "set_due_date", fake_set_due_date)

    response = client.post("/api/jira/webhook/?secret=test-secret", payload(), content_type="application/json")

    assert response.status_code == 200
    ticket = Ticket.objects.get(jira_key="OPS-9")
    assert ticket.priority == "P1"
    assert ticket.due_at == local(2026, 9, 14, 14, "America/Toronto")

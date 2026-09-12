from django.db import models

from calendar_rules.models import PRIORITIES, Country

SOURCES = [
    ("jira", "Jira"),
    ("email", "Email"),
]

PAUSED_STATUS = "Waiting for customer"


class Ticket(models.Model):
    jira_key = models.CharField(max_length=20, unique=True, null=True, blank=True)
    source = models.CharField(max_length=10, choices=SOURCES, default="jira")
    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=2, choices=PRIORITIES)
    status = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="tickets")
    created_at = models.DateTimeField()
    due_at = models.DateTimeField(null=True, blank=True)
    paused_minutes = models.PositiveIntegerField(default=0)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.jira_key or self.id} {self.title}"


class ClockEvent(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="clock_events")
    status_from = models.CharField(max_length=50)
    status_to = models.CharField(max_length=50)
    at = models.DateTimeField()

    class Meta:
        ordering = ["at"]

    def __str__(self):
        return f"{self.ticket} {self.status_from} to {self.status_to} at {self.at}"

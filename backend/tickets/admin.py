from django.contrib import admin

from .models import ClockEvent, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["jira_key", "title", "priority", "status", "country", "created_at", "due_at", "paused_minutes"]
    list_filter = ["country", "priority", "status"]


@admin.register(ClockEvent)
class ClockEventAdmin(admin.ModelAdmin):
    list_display = ["ticket", "status_from", "status_to", "at"]

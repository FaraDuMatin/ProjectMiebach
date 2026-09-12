from django.conf import settings
from django.core.management.base import BaseCommand

from jira_sync.client import JiraClient
from jira_sync.sync import sync_issue


class Command(BaseCommand):
    help = "Pull every issue of the Jira project, update tickets, write due dates back to Jira"

    def handle(self, *args, **options):
        client = JiraClient()
        issues = client.search_issues(f"project = {settings.JIRA_PROJECT_KEY} ORDER BY created ASC")
        synced = 0
        skipped = 0
        for issue in issues:
            ticket = sync_issue(client, issue)
            if ticket is None:
                skipped += 1
                self.stdout.write(f"{issue['key']} skipped, no country")
            else:
                synced += 1
                self.stdout.write(f"{ticket.jira_key} {ticket.priority} {ticket.country} due {ticket.due_at}")
        self.stdout.write(f"{synced} synced, {skipped} skipped")

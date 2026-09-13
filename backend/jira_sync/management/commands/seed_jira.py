from django.conf import settings
from django.core.management.base import BaseCommand

from jira_sync.client import JiraClient
from tickets.models import Ticket

DEMO_ISSUES = [
    ("Warehouse scan guns offline in Mississauga", "Highest", "CA"),
    ("Carrier rate import rejects CSV", "High", "CA"),
    ("Inventory count report shows negative stock", "Medium", "CA"),
    ("Add French labels to picking screen", "Low", "CA"),
    ("Dock scheduling page times out", "High", "CA"),
    ("Slotting export missing pallet height", "Medium", "CA"),
    ("Request read access for new analyst", "Low", "CA"),
    ("WMS interface down at Hamburg site", "Highest", "DE"),
    ("Customs document template outdated", "High", "DE"),
    ("Forecast dashboard slow on Monday morning", "Medium", "DE"),
    ("Rename cost center in transport model", "Low", "DE"),
    ("Duplicate shipments after ERP sync", "Highest", "DE"),
    ("Add KPI for truck fill rate", "Medium", "DE"),
    ("Login page shows wrong logo", "Lowest", "DE"),
    ("Order allocation stuck for Pune plant", "Highest", "IN"),
    ("Route optimizer ignores toll roads", "High", "IN"),
    ("Monthly capacity report wrong units", "Medium", "IN"),
    ("Onboard vendor to supplier portal", "Low", "IN"),
    ("Barcode labels print blurry", "Medium", "IN"),
    ("Timezone wrong on shift planning screen", "High", "IN"),
]


class Command(BaseCommand):
    help = "Create 20 demo issues in Jira. --clear deletes every issue of the project and every local ticket first."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        client = JiraClient()
        if options["clear"]:
            for issue in client.search_issues(f"project = {settings.JIRA_PROJECT_KEY}"):
                client.delete_issue(issue["key"])
                self.stdout.write(f"deleted {issue['key']}")
            Ticket.objects.all().delete()
        for title, priority, country in DEMO_ISSUES:
            key = client.create_issue(title, priority, country)
            self.stdout.write(f"created {key} {priority} {country} {title}")
        self.stdout.write("done, now run: python manage.py sync_jira")

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from .client import JiraClient
from .sync import sync_issue


class JiraWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        secret = request.query_params.get("secret")
        if not settings.JIRA_WEBHOOK_SECRET or secret != settings.JIRA_WEBHOOK_SECRET:
            return Response(status=403)

        issue = request.data.get("issue")
        if issue is None:
            return Response(status=400)

        ticket = sync_issue(JiraClient(), issue)
        if ticket is None:
            return Response({"skipped": issue["key"]})
        return Response({"ticket": ticket.jira_key, "due_at": ticket.due_at})

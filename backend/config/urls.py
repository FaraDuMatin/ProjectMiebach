from django.contrib import admin
from django.urls import path

from jira_sync.views import JiraWebhookView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/jira/webhook/", JiraWebhookView.as_view()),
]

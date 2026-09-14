from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from accounts.views import LoginView, LogoutView, MeView
from calendar_rules.views import CountryListView
from jira_sync.views import JiraWebhookView
from tickets.views import StatsView, TicketListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", LoginView.as_view()),
    path("api/auth/logout/", LogoutView.as_view()),
    path("api/auth/me/", MeView.as_view()),
    path("api/tickets/", TicketListView.as_view()),
    path("api/countries/", CountryListView.as_view()),
    path("api/stats/", StatsView.as_view()),
    path("api/jira/webhook/", JiraWebhookView.as_view()),
    path("", TemplateView.as_view(template_name="index.html")),
]

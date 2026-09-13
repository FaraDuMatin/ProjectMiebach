import django_filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DONE_STATUS, Ticket
from .serializers import TicketSerializer
from .sla import bucket

BUCKETS = ["at_risk", "on_time", "breached", "paused"]


class TicketFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name="country__code")

    class Meta:
        model = Ticket
        fields = ["status", "priority", "country"]


def tickets_with_due_date():
    return Ticket.objects.select_related("country").exclude(due_at=None).exclude(status=DONE_STATUS).order_by("due_at")


class TicketListView(ListAPIView):
    serializer_class = TicketSerializer
    filterset_class = TicketFilter

    def get_queryset(self):
        queryset = tickets_with_due_date()
        wanted = self.request.query_params.get("bucket")
        if wanted:
            ids = []
            for ticket in queryset:
                if bucket(ticket) == wanted:
                    ids.append(ticket.id)
            queryset = queryset.filter(id__in=ids)
        return queryset


class StatsView(APIView):
    def get(self, request):
        by_country = {}
        by_bucket = {}
        for name in BUCKETS:
            by_bucket[name] = 0
        for ticket in tickets_with_due_date():
            code = ticket.country.code
            by_country[code] = by_country.get(code, 0) + 1
            by_bucket[bucket(ticket)] += 1
        return Response({"by_country": by_country, "by_bucket": by_bucket})

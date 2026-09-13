from rest_framework.generics import ListAPIView

from .models import Country
from .serializers import CountrySerializer


class CountryListView(ListAPIView):
    queryset = Country.objects.order_by("code")
    serializer_class = CountrySerializer

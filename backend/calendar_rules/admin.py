from django.contrib import admin

from .models import Country, Holiday, SlaPolicy


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "timezone", "workday_start", "workday_end", "working_days"]


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ["country", "date", "name"]
    list_filter = ["country"]


@admin.register(SlaPolicy)
class SlaPolicyAdmin(admin.ModelAdmin):
    list_display = ["country", "priority", "hours"]
    list_filter = ["country", "priority"]

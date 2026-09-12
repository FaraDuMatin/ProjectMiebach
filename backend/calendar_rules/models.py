from django.db import models

PRIORITIES = [
    ("P1", "P1"),
    ("P2", "P2"),
    ("P3", "P3"),
    ("P4", "P4"),
]


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)
    workday_start = models.TimeField()
    workday_end = models.TimeField()
    # Weekday numbers separated by commas, Monday is 0
    working_days = models.CharField(max_length=20, default="0,1,2,3,4")

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.code

    def working_day_numbers(self):
        numbers = []
        for part in self.working_days.split(","):
            numbers.append(int(part))
        return numbers


class Holiday(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="holidays")
    date = models.DateField()
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ["country", "date"]

    def __str__(self):
        return f"{self.country.code} {self.date} {self.name}"


class SlaPolicy(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="policies")
    priority = models.CharField(max_length=2, choices=PRIORITIES)
    hours = models.PositiveIntegerField()

    class Meta:
        unique_together = ["country", "priority"]
        verbose_name_plural = "SLA policies"

    def __str__(self):
        return f"{self.country.code} {self.priority} {self.hours}h"

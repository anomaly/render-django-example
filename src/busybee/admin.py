from django.contrib import admin

from .models import City, DailyWeatherSummary, HourlyWeather


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "timezone", "created_at")
    search_fields = ("name", "country")


@admin.register(HourlyWeather)
class HourlyWeatherAdmin(admin.ModelAdmin):
    list_display = ("city", "observed_at", "temperature_c", "condition")
    list_filter = ("city", "condition")
    date_hierarchy = "observed_at"


@admin.register(DailyWeatherSummary)
class DailyWeatherSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "date",
        "temperature_min_c",
        "temperature_max_c",
        "precipitation_total_mm",
        "dominant_condition",
    )
    list_filter = ("city", "dominant_condition")
    date_hierarchy = "date"

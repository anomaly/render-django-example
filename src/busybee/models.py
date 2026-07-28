# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Allows us to extend the default user model to add application specific
    behaviour.

    See the following guide where it's easier to abstract user at the start
    of the project:

    https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    """

    pass


class City(models.Model):
    """
    A city the user can pick to generate weather data for.

    Kept intentionally light: enough to identify a place and seed
    plausible readings (latitude drives temperature ranges, timezone
    anchors the hourly timestamps).
    """

    name = models.CharField(max_length=128)
    country = models.CharField(
        max_length=2, help_text="ISO 3166-1 alpha-2 country code, e.g. AU."
    )
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    timezone = models.CharField(
        max_length=64,
        default="UTC",
        help_text="IANA timezone name, e.g. Australia/Sydney.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "cities"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("name", "country"), name="unique_city_per_country"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}, {self.country}"


class HourlyWeather(models.Model):
    """
    A single hourly weather reading for a city.

    A full year of fake data is 365 * 24 = 8,760 rows per city. The
    (city, observed_at) pair is unique so a populate workflow can be
    re-run idempotently, and is indexed for range queries when a
    downstream workflow aggregates readings into daily summaries.
    """

    class Condition(models.TextChoices):
        CLEAR = "clear", "Clear"
        PARTLY_CLOUDY = "partly_cloudy", "Partly cloudy"
        CLOUDY = "cloudy", "Cloudy"
        RAIN = "rain", "Rain"
        THUNDERSTORM = "thunderstorm", "Thunderstorm"
        SNOW = "snow", "Snow"
        FOG = "fog", "Fog"

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="hourly_readings"
    )
    observed_at = models.DateTimeField(
        help_text="Start of the hour this reading covers, in UTC."
    )

    temperature_c = models.FloatField(help_text="Air temperature in degrees Celsius.")
    feels_like_c = models.FloatField(
        null=True, blank=True, help_text="Apparent temperature in degrees Celsius."
    )
    humidity = models.PositiveSmallIntegerField(help_text="Relative humidity, 0-100%.")
    pressure_hpa = models.FloatField(help_text="Sea-level pressure in hectopascals.")
    wind_speed_kph = models.FloatField(help_text="Wind speed in km/h.")
    wind_direction_deg = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Wind bearing, 0-359 degrees."
    )
    precipitation_mm = models.FloatField(
        default=0, help_text="Precipitation over the hour in millimetres."
    )
    cloud_cover = models.PositiveSmallIntegerField(
        default=0, help_text="Cloud cover, 0-100%."
    )
    condition = models.CharField(
        max_length=16, choices=Condition.choices, default=Condition.CLEAR
    )

    class Meta:
        verbose_name_plural = "hourly weather"
        ordering = ("city", "observed_at")
        constraints = [
            models.UniqueConstraint(
                fields=("city", "observed_at"), name="unique_reading_per_city_hour"
            )
        ]
        indexes = [
            models.Index(
                fields=("city", "observed_at"), name="weather_city_hour_idx"
            )
        ]

    def __str__(self) -> str:
        return f"{self.city} @ {self.observed_at:%Y-%m-%d %H:00}"


class DailyWeatherSummary(models.Model):
    """
    A daily rollup of a city's hourly readings.

    This is the output of the aggregate workflow: it collapses the 24
    hourly rows for a given day into a single summary. Unique on
    (city, date) so the aggregate can be re-run idempotently.
    """

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="daily_summaries"
    )
    date = models.DateField(help_text="The calendar day this summary covers.")

    temperature_min_c = models.FloatField()
    temperature_max_c = models.FloatField()
    temperature_mean_c = models.FloatField()
    humidity_mean = models.FloatField(help_text="Mean relative humidity, 0-100%.")
    pressure_mean_hpa = models.FloatField()
    wind_speed_max_kph = models.FloatField()
    precipitation_total_mm = models.FloatField(
        help_text="Total precipitation over the day in millimetres."
    )
    dominant_condition = models.CharField(
        max_length=16,
        choices=HourlyWeather.Condition.choices,
        help_text="The most frequent hourly condition for the day.",
    )
    reading_count = models.PositiveSmallIntegerField(
        default=0, help_text="Number of hourly readings this summary is based on."
    )

    class Meta:
        verbose_name_plural = "daily weather summaries"
        ordering = ("city", "date")
        constraints = [
            models.UniqueConstraint(
                fields=("city", "date"), name="unique_summary_per_city_day"
            )
        ]
        indexes = [
            models.Index(fields=("city", "date"), name="weather_city_day_idx")
        ]

    def __str__(self) -> str:
        return f"{self.city} on {self.date:%Y-%m-%d}"

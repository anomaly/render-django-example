import math
import random
from datetime import datetime, timedelta, timezone

from asgiref.sync import sync_to_async
from render_sdk import Workflows

from busybee.models import City, HourlyWeather

app = Workflows()

@app.task
async def populate_city_weather(city_id: int, year: int = 2025) -> int:
    """
    Generate a full year of fake hourly weather for a city.

    Produces one HourlyWeather row per hour of ``year`` (8,760 rows, or
    8,784 in a leap year). Existing rows for that city and year are
    deleted first so the task is idempotent and safe to re-run.

    Returns the number of rows created.
    """
    with logfire.span("populate_city_weather", city_id=city_id, year=year):
        city = await City.objects.aget(pk=city_id)

        readings = await sync_to_async(_build_year)(city, year)

        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        deleted, _ = await HourlyWeather.objects.filter(
            city=city, observed_at__gte=start, observed_at__lt=end
        ).adelete()
        if deleted:
            logfire.info("Cleared existing readings", deleted=deleted)

        await HourlyWeather.objects.abulk_create(readings, batch_size=1000)
        logfire.info("Populated readings", created=len(readings))
        return len(readings)


def _build_year(city: City, year: int) -> list[HourlyWeather]:
    """Build (but do not save) an hourly reading for every hour of the year."""
    latitude = float(city.latitude)
    start = datetime(year, 1, 1, tzinfo=timezone.utc)
    end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)

    readings: list[HourlyWeather] = []
    current = start
    while current < end:
        day_of_year = current.timetuple().tm_yday
        readings.append(_build_reading(city, current, latitude, day_of_year))
        current += timedelta(hours=1)
    return readings


def _build_reading(
    city: City, observed_at: datetime, latitude: float, day_of_year: int
) -> HourlyWeather:
    """Sample a single, roughly plausible hourly reading."""
    hour = observed_at.hour

    # Annual mean falls toward the poles; seasonal swing grows with latitude
    # and flips phase between hemispheres (warmest in July up north, January
    # down south). A diurnal term makes ~3pm the warmest hour, ~5am the coldest.
    abs_lat = abs(latitude)
    annual_mean = 27.0 - 0.007 * abs_lat**2
    seasonal_amp = 2.0 + 0.22 * abs_lat
    peak_day = 202.0 if latitude >= 0 else 202.0 - 182.5
    seasonal = seasonal_amp * math.cos(2 * math.pi * (day_of_year - peak_day) / 365.0)
    diurnal = 5.0 * math.cos(2 * math.pi * (hour - 15) / 24.0)

    temperature = round(annual_mean + seasonal + diurnal + random.gauss(0, 1.5), 1)

    # Cloud cover drives condition and precipitation; humidity rises with cloud.
    cloud_cover = min(100, max(0, int(random.gauss(45, 30))))
    humidity = min(100, max(15, int(50 + cloud_cover * 0.35 + random.gauss(0, 8))))
    pressure = round(random.gauss(1013, 7), 1)
    wind_speed = round(abs(random.gauss(12, 7)), 1)
    wind_direction = random.randint(0, 359)

    precipitation = 0.0
    if cloud_cover > 60 and random.random() < (cloud_cover - 60) / 60:
        precipitation = round(abs(random.gauss(1.5, 2.0)), 1)

    condition = _condition_for(temperature, cloud_cover, precipitation)

    # A crude apparent-temperature nudge: wind chills, humidity warms.
    feels_like = round(
        temperature - wind_speed * 0.05 + (humidity - 50) * 0.02, 1
    )

    return HourlyWeather(
        city=city,
        observed_at=observed_at,
        temperature_c=temperature,
        feels_like_c=feels_like,
        humidity=humidity,
        pressure_hpa=pressure,
        wind_speed_kph=wind_speed,
        wind_direction_deg=wind_direction,
        precipitation_mm=precipitation,
        cloud_cover=cloud_cover,
        condition=condition,
    )


def _condition_for(
    temperature: float, cloud_cover: int, precipitation: float
) -> str:
    """Pick a condition consistent with the sampled metrics."""
    Condition = HourlyWeather.Condition
    if precipitation > 0:
        if temperature <= 0:
            return Condition.SNOW
        return Condition.THUNDERSTORM if precipitation > 4 else Condition.RAIN
    if cloud_cover >= 80:
        return Condition.CLOUDY
    if cloud_cover >= 40:
        return Condition.PARTLY_CLOUDY
    return Condition.CLEAR

import pytest

from weather import get_forecast

@pytest.mark.asyncio
async def test_get_forecast():
    # Test with valid coordinates (e.g., New York City)
    latitude = 40.7128
    longitude = -74.0060
    forecast = await get_forecast(latitude, longitude)
    print(forecast)
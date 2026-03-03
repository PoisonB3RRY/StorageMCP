import pytest
from unittest.mock import patch, AsyncMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from server import get_alerts, get_forecast, make_nws_request, mcp


class TestWeatherTools:
    """Test cases for the MCP weather tools."""

    @pytest.mark.asyncio
    async def test_get_alerts_with_active_alerts(self):
        """Test get_alerts with active alerts."""
        mock_data = {
            "features": [
                {
                    "properties": {
                        "event": "Severe Thunderstorm Warning",
                        "areaDesc": "San Francisco County",
                        "severity": "Severe",
                        "description": "Severe thunderstorm warning in effect",
                        "instruction": "Take shelter immediately"
                    }
                }
            ]
        }
        
        with patch("server.make_nws_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_data
            result = await get_alerts("CA")
            assert "Severe Thunderstorm Warning" in result
            assert "San Francisco County" in result

    @pytest.mark.asyncio
    async def test_get_alerts_no_alerts(self):
        """Test get_alerts with no active alerts."""
        mock_data = {"features": []}
        
        with patch("server.make_nws_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_data
            result = await get_alerts("CA")
            assert "No active weather alerts" in result

    @pytest.mark.asyncio
    async def test_get_alerts_error(self):
        """Test get_alerts with API error."""
        with patch("server.make_nws_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            result = await get_alerts("CA")
            assert "Failed to retrieve weather alerts" in result

    @pytest.mark.asyncio
    async def test_get_forecast_success(self):
        """Test successful forecast request."""
        mock_points_data = {
            "properties": {
                "forecast": "https://api.weather.gov/gridpoints/MTR/84,105/forecast"
            }
        }
        mock_forecast_data = {
            "properties": {
                "periods": [
                    {
                        "name": "Today",
                        "temperature": 75,
                        "temperatureUnit": "F",
                        "windSpeed": "10 mph",
                        "windDirection": "NW",
                        "detailedForecast": "Sunny and warm"
                    }
                ]
            }
        }
        
        with patch("server.make_nws_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [mock_points_data, mock_forecast_data]
            result = await get_forecast(37.7749, -122.4194)
            assert "Today" in result
            assert "75" in result

    @pytest.mark.asyncio
    async def test_get_forecast_error(self):
        """Test forecast request with error."""
        with patch("server.make_nws_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            result = await get_forecast(37.7749, -122.4194)
            assert "Unable to fetch forecast data" in result


class TestMCPServer:
    """Test cases for MCP server configuration."""

    def test_mcp_server_name(self):
        """Test that MCP server has correct name."""
        assert mcp.name == "weather"

    def test_tools_registered(self):
        """Test that tools are registered."""
        tools = mcp._tool_manager._tools
        assert "get_alerts" in tools
        assert "get_forecast" in tools

    def test_prompts_registered(self):
        """Test that prompts are registered."""
        prompts = mcp._prompt_manager._prompts
        assert "weather_query" in prompts
        assert "weather_analysis" in prompts
        assert "weather_report" in prompts
        assert "alert_summary" in prompts
        assert "daily_briefing" in prompts

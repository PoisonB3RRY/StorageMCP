import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from server import app

client = TestClient(app)


class TestServer:
    """Test cases for the MCP server."""

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "weather-mcp-server"

    def test_get_tools(self):
        """Test the tools endpoint."""
        response = client.get("/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert len(data["tools"]) == 2
        
        tools = data["tools"]
        tool_names = [tool["name"] for tool in tools]
        assert "get_forecast" in tool_names
        assert "get_alerts" in tool_names

    @patch("server.get_forecast")
    def test_get_forecast_success(self, mock_get_forecast):
        """Test successful forecast request."""
        mock_result = {
            "forecast": [
                {"period": "Today", "temperature": "75F", "description": "Sunny"},
                {"period": "Tonight", "temperature": "55F", "description": "Clear"},
            ]
        }
        mock_get_forecast.return_value = mock_result

        response = client.post(
            "/forecast",
            json={"latitude": 37.7749, "longitude": -122.4194}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] == mock_result
        mock_get_forecast.assert_called_once_with(37.7749, -122.4194)

    @patch("server.get_forecast")
    def test_get_forecast_error(self, mock_get_forecast):
        """Test forecast request with error."""
        mock_get_forecast.side_effect = Exception("API Error")

        response = client.post(
            "/forecast",
            json={"latitude": 37.7749, "longitude": -122.4194}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "API Error" in data["error"]

    @patch("server.get_alerts")
    def test_get_alerts_success(self, mock_get_alerts):
        """Test successful alerts request."""
        mock_result = {
            "alerts": [
                {"event": "Severe Thunderstorm Warning", "severity": "Severe"},
                {"event": "Flash Flood Watch", "severity": "Moderate"},
            ]
        }
        mock_get_alerts.return_value = mock_result

        response = client.post(
            "/alerts",
            json={"state": "CA"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] == mock_result
        mock_get_alerts.assert_called_once_with("CA")

    @patch("server.get_alerts")
    def test_get_alerts_error(self, mock_get_alerts):
        """Test alerts request with error."""
        mock_get_alerts.side_effect = Exception("Invalid state")

        response = client.post(
            "/alerts",
            json={"state": "XX"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "Invalid state" in data["error"]

    def test_forecast_invalid_request(self):
        """Test forecast request with invalid data."""
        response = client.post(
            "/forecast",
            json={"latitude": "invalid", "longitude": -122.4194}
        )
        assert response.status_code == 422  # Validation error

    def test_alerts_invalid_request(self):
        """Test alerts request with invalid data."""
        response = client.post(
            "/alerts",
            json={"state": 123}
        )
        assert response.status_code == 422  # Validation error
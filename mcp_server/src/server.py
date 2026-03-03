import logging
import os
import sys
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

sys.path.insert(0, os.path.dirname(__file__));

from config import get_settings

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("weather")

NWS_API_BASE = settings.weather_api_base_url
USER_AGENT = settings.user_agent


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API to get weather data."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch weather data from NWS API: {str(e)}")
            return {"error": f"Failed to fetch weather data from NWS API: {str(e)}"}


def format_alert(feature: dict[str, Any]) -> str:
    """Format a weather alert into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: The US state to get alerts for (e.g., 'CA' for California).
    """
    logger.info(f"Getting alerts for state={state}")
    url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "Failed to retrieve weather alerts. Please try again later."
    
    if not data["features"]:
        return f"No active weather alerts for {state.upper()}."
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
    """
    logger.info(f"Getting forecast for lat={latitude}, lon={longitude}")
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data or "properties" not in points_data:
        return "Unable to fetch forecast data for this location."

    if "error" in points_data:
        return points_data["error"]

    forecast_url = points_data["properties"].get("forecast")
    if not forecast_url:
        return "Unable to get forecast URL from points data."

    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data or "properties" not in forecast_data:
        return "Unable to fetch detailed forecast."

    periods = forecast_data["properties"].get("periods", [])
    if not periods:
        return "No forecast periods available."

    forecasts = []
    for period in periods[:5]:
        forecast = f"""
{period.get("name", "Unknown")}:
Temperature: {period.get("temperature", "N/A")}°{period.get("temperatureUnit", "F")}
Wind: {period.get("windSpeed", "N/A")} {period.get("windDirection", "")}
Forecast: {period.get("detailedForecast", "No detailed forecast available")}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.prompt()
def weather_query(location: str, days: str = "3") -> str:
    """Query weather for a specific location.

    Args:
        location: Location name or coordinates.
        days: Number of forecast days (default 3).
    """
    return f"Please check the weather for {location} and provide the forecast for the next {days} days. Include temperature, humidity, wind speed, and precipitation probability."


@mcp.prompt()
def weather_analysis(location: str, data: str) -> str:
    """Analyze weather data and provide professional advice.

    Args:
        location: Location name.
        data: Weather data to analyze.
    """
    return f"""Based on the following weather data, please provide a professional analysis for {location}:

{data}

Please provide:
1. Weather trend analysis
2. Impact assessment for travel
3. Relevant recommendations"""


@mcp.prompt()
def weather_report(location: str, period: str) -> str:
    """Generate a professional weather report.

    Args:
        location: Location name.
        period: Time period for the report.
    """
    return f"""Please generate a professional weather report for {location} covering the {period} period. The report should include:

1. Overall weather summary
2. Temperature trends
3. Precipitation statistics
4. Wind direction and speed analysis
5. Special weather events
6. Recommendations for local residents"""


@mcp.prompt()
def alert_summary(state: str, alerts: str) -> str:
    """Generate a weather alert summary.

    Args:
        state: State or region name.
        alerts: Alert data.
    """
    return f"""Please generate a weather alert summary for {state}:

{alerts}

Please include:
1. Alert type statistics
2. Impact area analysis
3. Duration assessment
4. Safety recommendations"""


@mcp.prompt()
def daily_briefing(location: str) -> str:
    """Generate a daily weather briefing.

    Args:
        location: Location name.
    """
    return f"""Please generate a daily weather briefing for {location}, including:

1. Today's weather overview
2. Temperature range
3. Precipitation probability
4. Wind conditions
5. Air quality
6. Travel recommendations
7. Clothing suggestions"""


@mcp.resource("weather://config")
def get_config() -> str:
    """Get the server configuration."""
    return f"""Weather MCP Server Configuration:
- API Base URL: {NWS_API_BASE}
- User Agent: {USER_AGENT}
- Log Level: {settings.log_level}
"""


def run_sse_server():
    """Run the MCP server with SSE transport."""
    import uvicorn
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route

    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as (read_stream, write_stream):
            await mcp._mcp_server.run(
                read_stream, write_stream, mcp._mcp_server.create_initialization_options()
            )

    async def handle_messages(request):
        await sse.handle_post_message(request._receive, request._send)

    app = Starlette(
        debug=settings.debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages", endpoint=handle_messages, methods=["POST"]),
        ],
    )

    uvicorn.run(app, host=settings.host, port=settings.port)

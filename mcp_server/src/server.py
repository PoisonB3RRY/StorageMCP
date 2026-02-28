import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add the parent directory to sys.path to import weather module
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from weather import get_forecast, get_alerts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("mcp_server.log"),
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Weather MCP Server",
    description="MCP server for weather forecasting and alerts",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ForecastRequest(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")


class AlertsRequest(BaseModel):
    state: str = Field(..., description="US state to get alerts for (e.g., 'CA')")


class MCPResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


@app.post("/forecast", response_model=MCPResponse)
async def get_weather_forecast(request: ForecastRequest):
    """
    Get weather forecast for a location.
    """
    try:
        logger.info(f"Getting forecast for lat={request.latitude}, lon={request.longitude}")
        result = await asyncio.to_thread(
            get_forecast, request.latitude, request.longitude
        )
        return MCPResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Error getting forecast: {str(e)}")
        return MCPResponse(success=False, error=str(e))


@app.post("/alerts", response_model=MCPResponse)
async def get_weather_alerts(request: AlertsRequest):
    """
    Get weather alerts for a US state.
    """
    try:
        logger.info(f"Getting alerts for state={request.state}")
        result = await asyncio.to_thread(get_alerts, request.state)
        return MCPResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        return MCPResponse(success=False, error=str(e))


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "weather-mcp-server"}


@app.get("/tools")
async def get_tools():
    """
    Return available tools for MCP clients.
    """
    tools = [
        {
            "name": "get_forecast",
            "description": "Get weather forecast for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location",
                    },
                },
                "required": ["latitude", "longitude"],
            },
        },
        {
            "name": "get_alerts",
            "description": "Get weather alerts for a US state",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "US state to get alerts for (e.g., 'CA')",
                    },
                },
                "required": ["state"],
            },
        },
    ]
    return {"tools": tools}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
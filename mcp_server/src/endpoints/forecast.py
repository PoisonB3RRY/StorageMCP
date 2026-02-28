import asyncio
import logging
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))
from responses import MCPResponse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from weather import get_forecast

logger = logging.getLogger(__name__)

async def get_weather_forecast(request: BaseModel) -> MCPResponse:
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
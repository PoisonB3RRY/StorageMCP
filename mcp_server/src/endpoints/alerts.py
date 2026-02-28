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
from weather import get_alerts

logger = logging.getLogger(__name__)

async def get_weather_alerts(request: BaseModel) -> MCPResponse:
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
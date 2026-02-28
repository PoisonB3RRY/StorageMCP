from typing import Any, Dict, List

from fastapi import HTTPException
from pydantic import BaseModel

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))
from responses import MCPResponse

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
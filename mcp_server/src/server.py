import logging
import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the parent directory to sys.path to import weather module
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from weather import get_forecast, get_alerts

# Import endpoints
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "endpoints"))
from alerts import get_weather_alerts
from forecast import get_weather_forecast
from health import health_check
from tools import get_tools
from prompts import get_prompt_templates, get_prompt_template, get_prompt_categories, PromptRequest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "models"))
from responses import AlertsRequest, ForecastRequest, MCPResponse

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


@app.post("/forecast", response_model=MCPResponse)
async def forecast_endpoint(request: ForecastRequest):
    """
    Get weather forecast for a location.
    """
    return await get_weather_forecast(request)


@app.post("/alerts", response_model=MCPResponse)
async def alerts_endpoint(request: AlertsRequest):
    """
    Get weather alerts for a US state.
    """
    return await get_weather_alerts(request)


@app.get("/health")
async def health_endpoint():
    """
    Health check endpoint.
    """
    return await health_check()


@app.get("/tools")
async def tools_endpoint():
    """
    Return available tools for MCP clients.
    """
    return await get_tools()


@app.get("/prompts")
async def prompts_endpoint():
    """
    Return available prompt templates for MCP clients.
    """
    return await get_prompt_templates()


@app.get("/prompts/categories")
async def prompt_categories_endpoint():
    """
    Return prompt template categories.
    """
    return await get_prompt_categories()


@app.post("/prompts/{name}")
async def prompt_template_endpoint(name: str, request: PromptRequest):
    """
    Get a specific prompt template with optional parameter rendering.
    """
    request.name = name  # Set the name from path parameter
    return await get_prompt_template(request)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
from typing import Any, Optional
from pydantic import BaseModel, Field

class ForecastRequest(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")

class AlertsRequest(BaseModel):
    state: str = Field(..., description="US state to get alerts for (e.g., 'CA')")

class MCPResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
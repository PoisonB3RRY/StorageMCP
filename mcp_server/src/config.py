import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Weather API settings
    weather_api_base_url: str = "https://api.weather.gov"
    user_agent: str = "WeatherMCP/0.1.0"
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str = "mcp_server.log"
    
    # CORS settings
    allow_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_prefix = "MCP_"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
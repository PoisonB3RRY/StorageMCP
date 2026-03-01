from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ForecastRequest(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")

class AlertsRequest(BaseModel):
    state: str = Field(..., description="US state to get alerts for (e.g., 'CA')")

class PromptArgument(BaseModel):
    """提示模板参数定义"""
    name: str = Field(..., description="参数名称")
    description: str = Field(..., description="参数描述")
    required: bool = Field(True, description="是否必需")

class PromptTemplate(BaseModel):
    """提示模板定义"""
    name: str = Field(..., description="模板名称")
    description: str = Field(..., description="模板描述")
    arguments: List[PromptArgument] = Field(default_factory=list, description="模板参数列表")
    template: str = Field(..., description="提示模板内容")
    category: str = Field(default="general", description="模板分类")

class PromptRequest(BaseModel):
    """获取提示模板的请求"""
    name: str = Field(..., description="模板名称")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="参数值")

class PromptResponse(BaseModel):
    """提示模板响应"""
    success: bool
    data: Optional[PromptTemplate] = None
    rendered_template: Optional[str] = None
    error: Optional[str] = None

class MCPResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

import logging
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class PromptArgument(BaseModel):
    """提示模板参数定义"""
    name: str
    description: str
    required: bool = True

class PromptTemplate(BaseModel):
    """提示模板定义"""
    name: str
    description: str
    arguments: List[PromptArgument]
    template: str
    category: str = "general"

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

# 预定义的提示模板
PROMPT_TEMPLATES: Dict[str, PromptTemplate] = {
    "weather_query": PromptTemplate(
        name="weather_query",
        description="查询特定位置的天气情况",
        arguments=[
            PromptArgument(
                name="location",
                description="位置名称或坐标",
                required=True
            ),
            PromptArgument(
                name="days",
                description="预报天数（默认3天）",
                required=False
            )
        ],
        template="请查询 {location} 的当前天气情况和未来 {days} 天的天气预报。请提供温度、湿度、风速、降水概率等详细信息。",
        category="weather"
    ),
    
    "weather_analysis": PromptTemplate(
        name="weather_analysis",
        description="分析天气数据并提供专业建议",
        arguments=[
            PromptArgument(
                name="location",
                description="位置名称",
                required=True
            ),
            PromptArgument(
                name="data",
                description="天气数据",
                required=True
            )
        ],
        template="基于以下天气数据，请对 {location} 进行专业分析：\n\n{data}\n\n请提供：\n1. 天气趋势分析\n2. 对出行的影响评估\n3. 相关建议",
        category="analysis"
    ),
    
    "weather_report": PromptTemplate(
        name="weather_report",
        description="生成专业的天气报告",
        arguments=[
            PromptArgument(
                name="location",
                description="位置名称",
                required=True
            ),
            PromptArgument(
                name="period",
                description="报告时间段",
                required=True
            )
        ],
        template="请为 {location} 生成一份专业的天气报告，涵盖 {period} 期间的天气情况。报告应包括：\n\n1. 总体天气概况\n2. 温度变化趋势\n3. 降水情况统计\n4. 风力风向分析\n5. 特殊天气事件\n6. 对当地居民的建议",
        category="report"
    ),
    
    "alert_summary": PromptTemplate(
        name="alert_summary",
        description="生成天气警报摘要",
        arguments=[
            PromptArgument(
                name="state",
                description="州名或地区",
                required=True
            ),
            PromptArgument(
                name="alerts",
                description="警报数据",
                required=True
            )
        ],
        template="请为 {state} 生成天气警报摘要：\n\n{alerts}\n\n请包括：\n1. 警报类型统计\n2. 影响范围分析\n3. 持续时间评估\n4. 安全建议",
        category="alert"
    ),
    
    "daily_briefing": PromptTemplate(
        name="daily_briefing",
        description="生成每日天气简报",
        arguments=[
            PromptArgument(
                name="location",
                description="位置名称",
                required=True
            )
        ],
        template="请为 {location} 生成一份每日天气简报，包括：\n\n1. 今日天气概况\n2. 温度范围\n3. 降水概率\n4. 风力情况\n5. 空气质量\n6. 出行建议\n7. 穿衣建议",
        category="daily"
    )
}

async def get_prompt_templates() -> Dict[str, Any]:
    """
    获取所有可用的提示模板列表
    """
    try:
        templates_list = []
        for template in PROMPT_TEMPLATES.values():
            templates_list.append({
                "name": template.name,
                "description": template.description,
                "category": template.category,
                "template": template.template,
                "arguments": [arg.dict() for arg in template.arguments]
            })
        
        return {
            "success": True,
            "data": {
                "templates": templates_list,
                "total": len(templates_list)
            }
        }
    except Exception as e:
        logger.error(f"Error getting prompt templates: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

async def get_prompt_template(request: PromptRequest) -> PromptResponse:
    """
    获取指定的提示模板并可选地渲染参数
    """
    try:
        template_name = request.name
        parameters = request.parameters or {}
        
        if template_name not in PROMPT_TEMPLATES:
            raise HTTPException(
                status_code=404,
                detail=f"Prompt template '{template_name}' not found"
            )
        
        template = PROMPT_TEMPLATES[template_name]
        
        # 渲染模板（如果提供了参数）
        rendered_template = None
        if parameters:
            try:
                rendered_template = template.template.format(**parameters)
            except KeyError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required parameter: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Template rendering error: {str(e)}"
                )
        
        return PromptResponse(
            success=True,
            data=template,
            rendered_template=rendered_template
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting prompt template: {str(e)}")
        return PromptResponse(
            success=False,
            error=str(e)
        )

async def get_prompt_categories() -> Dict[str, Any]:
    """
    获取提示模板的分类列表
    """
    try:
        categories = {}
        for template in PROMPT_TEMPLATES.values():
            if template.category not in categories:
                categories[template.category] = []
            categories[template.category].append(template.name)
        
        return {
            "success": True,
            "data": categories
        }
    except Exception as e:
        logger.error(f"Error getting prompt categories: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
from langchain_core.tools import StructuredTool
# 导入工具出现异常的时候，处理的库
from langchain_core.tools import ToolException

def get_weather(city: str) -> int:
    """获取给定城市的天气"""
    raise ToolException(f"错误，没有名为{city}的城市。")

get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    # 默认情况下，如果函数抛出ToolException，则将ToolException的message作为响应。
    # 如果设置为True，则将返回ToolException异常文本，False将会抛出ToolException
    handle_tool_error=False,
)
response = get_weather_tool.invoke({"city": "测试"})
print(response)
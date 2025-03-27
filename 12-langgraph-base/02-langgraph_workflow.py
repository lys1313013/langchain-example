# 基于LangGraph实现用于执行复杂的多步骤任务。
# 根据用户输入的目标，生成一个逐步执行的家虎，并按照计划执行任务
"""
使用 planner_prompt 生成一个包含多个步骤的计划（Plan）。
通过 agent_executor 执行计划中的每一步。
每一步的执行结果会被记录下来，并用于更新状态。
"""
# 导入标准库
import os
import asyncio
import operator
from typing import Annotated, List, Tuple, TypedDict, Union, Literal

# 导入第三方库
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.globals import set_verbose
from langchain import hub
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, START
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

set_verbose(True)

os.environ["LANGCHAIN_TRACING_V2"] = "true"

# 创建TavilySearchResults工具，设置最大结果数
tools = [TavilySearchResults(max_results=1)]


# 从LangChain的Hub中获取prompt模板，可以进行修改
prompt = hub.pull("wfh/react-agent-executor")
prompt.pretty_print()

# 从LangChain的Hub中获取模型，可以进行修改
llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)
agent_executor = create_react_agent(llm, tools)

class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str
    # 添加类型标注
    __annotations__ = {
        "input": str,
        "plan": List[str],
        "past_steps": List[Tuple],
        "response": str
    }

class Plan(BaseModel):
    """未来要执行的计划"""
    steps: List[str] = Field(
        description="需要执行的不同步骤，应该按顺序排列"
    )

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
         """对于给定目标，提出一个简单的逐步计划（请用JSON格式返回结果）。这个计划应该包含独立的任务，如果正确执行将得到正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。确保每一步都有所有必要的信息 - 不要跳过步骤。返回的JSON必须包含一个名为"steps"的字段，该字段是一个字符串列表。"""
        ),
        ("placeholder", "{messages}"),
    ]
)
# 使用指定的提示模板创建一个计划生成器
planner = planner_prompt | ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
).with_structured_output(Plan)

from typing import Union

class Response(BaseModel):
    """用户响应"""
    response: str

# 定义一个行为模型类，用于描述要执行的行为。该类继承自BaseModel
# 类中有一个属性action，类行为Union[Response, Plan], 表示可以是Response 或 Plan类型
# action 属性的描述为：要执行的行为。如果要回应用户，使用Response: 如果需要进一步使用工具获取答案，使用Plan
class Act(BaseModel):
    action: Union[Response, Plan] = Field(
        description="要执行的行为。如果已经得到最终的答案，要回复用户，使用Response: 如果需要进一步使用工具获取答案，使用Plan"
    )

# 创建一个重新计划的提示模板
replanner_prompt = ChatPromptTemplate.from_template(
    """
    对于给定目标，提出一个简单的逐步计划。这个计划应该包含独立的任务，如果正确执行将得到正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。确保每一步都有所有必要的信息 - 不要跳过步骤。

    你的目标是：
    {input}

    你的原计划是：
    {plan}

    你目前已完成的步骤是：
    {past_steps}

    响应的更新你的计划。如果已经得到最终答案，要给用户相应结果，请使用以下格式：
    {{"action": {{"response": <最终答案>}}}}
    
    如果需要继续执行，请使用以下格式：
    {{"action": {{"steps": ["剩余步骤1", "剩余步骤2"]}}}}    
    
    请以 JSON 格式返回结果。
    """
)

replanner = replanner_prompt | ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0
).with_structured_output(Act, method="json_mode")

from typing import Literal

# 定义一个异步主函数
async def main():
    # 定义一个异步函数，用于生成计划步骤
    async def plan_step(state: PlanExecute):
        # plan = await planner.ainvoke({"messages": [{"user": state["input"]}]})
        # return {"plan": plan.steps}
        plan = await planner.ainvoke({"messages": [{"role": "user", "content": state["input"]}]})
        return {"plan": plan.steps, "past_steps": state.get("past_steps", [])}

    # 定义一个异步函数，用于执行步骤
    async def execute_step(state: PlanExecute):
        plan = state["plan"]
        plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan))
        task = plan[0]
        task_formatted = f"""对于以下计划：
{plan_str}\n\n你的任务是执行第{1}步，{task}。"""
        agent_response = await agent_executor.ainvoke(
            {"messages": [("user", task_formatted)]}
        )
        return {
            "past_steps": state["past_steps"] + [(task, agent_response["messages"][-1].content)],
        }

    # # 定义一个异步函数，用于从新计划步骤
    # async def replan_step(state: PlanExecute):
    #     output = await replanner.ainvoke(state)
    #     print(output)  # 打印返回的 JSON 数据
    #     if isinstance(output.action, Response):
    #         return {"response": output.action.response}
    #     else:
    #         return {"plan": output.action.steps}

    async def replan_step(state: PlanExecute):
        output = await replanner.ainvoke(state)
        if isinstance(output.action, Response):
            return {"response": output.action.response}
        else:
            return {"plan": output.action.steps}

    # 定义一个函数，用于判断是否结束
    def should_end(state: PlanExecute) -> Literal["agent", "__end__"]:
        if "response" in state and state["response"]:
            return "__end__"
        else:
            return "agent"

    # 创建一个状态图，初始化PlanExecute
    workflow = StateGraph(PlanExecute)

    # 添加计划节点
    workflow.add_node("planner", plan_step)

    # 添加执行步骤节点
    workflow.add_node("agent", execute_step)

    # 添加重新计划节点
    workflow.add_node("replan", replan_step)

    # 设置从开始到计划节点的边
    workflow.add_edge(START, "planner")

    # 设置从计划到代理节点的边
    workflow.add_edge("planner", "agent")

    # 设置从代理到重新计划节点的边
    workflow.add_edge("agent", "replan")

    # 添加条件边，用于判断下一步操作
    workflow.add_conditional_edges(
        "replan",
        # 传入判断函数，确定下一个节点
        should_end
    )

    # 编译状态图，生成LangChain可运行对象
    app = workflow.compile()

    # 将生成的图片保存到文件
    graph_png = app.get_graph().draw_mermaid_png()
    with open("langgraph_workflow.png", "wb") as f:
        f.write(graph_png)

    # 设置配置，递归限制为50
    config = {"recursion_limit": 50}
    # 输入数据
    inputs = {"input": "2024年巴黎奥运会100米自由泳决赛冠军的家乡是哪里？请用中文回答"}
    # 异步执行状态图，输出结果
    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(v)

# 运行异步函数
asyncio.run(main())


# 输出结果示例(回答存在随机性)
"""

================================ System Message ================================

You are a helpful assistant.

============================= Messages Placeholder =============================

{{messages}}
{'plan': ['查询2024年巴黎奥运会100米自由泳决赛的冠军是谁。', '查找该冠军运动员的个人资料，包括他们的家乡。', '确认并提供该运动员的家乡所在地。'], 'past_steps': []}
{'past_steps': [('查询2024年巴黎奥运会100米自由泳决赛的冠军是谁。', '2024年巴黎奥运会100米自由泳决赛的冠军是潘展乐，他代表中国参赛，并且创造了46.40秒的新世界纪录成绩。')]}
{'plan': ['查找该冠军运动员潘展乐的个人资料，包括他们的家乡。', '确认并提供该运动员的家乡所在地。']}
{'past_steps': [('查询2024年巴黎奥运会100米自由泳决赛的冠军是谁。', '2024年巴黎奥运会100米自由泳决赛的冠军是潘展乐，他代表中国参赛，并且创造了46.40秒的新世界纪录成绩。'), ('查找该冠军运动员潘展乐的个人资料，包括他们的家乡。', '潘展乐是中国的一位著名男子游泳运动员，他出生于2004年8月4日，并且是浙江省温州市永嘉县人。他是自由泳项目的佼佼者，也是100米自由泳世界纪录保持者。')]}
{'response': '2024年巴黎奥运会100米自由泳决赛冠军潘展乐的家乡是中国浙江省温州市永嘉县。'}
"""
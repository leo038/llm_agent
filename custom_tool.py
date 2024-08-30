"""
crewAI中已经实现好了很多现成的tool可供使用。 https://docs.crewai.com/core-concepts/Tools/
开发自己的tool之前可以先看看是否有满足需求的，尽量不要造重复的轮子。
在crewAI中实现自己的tools也很简单， 有2种方式， 一种是继承BaseTool类， 另一种是自己写个函数， 用tool 这个装饰器包装这个函数
"""

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, tool


@tool
def my_tool(num1: int, num2: int) -> int:
    """Useful for when you need to add two numbers together."""

    return num1 + num2


search_tool = SerperDevTool()
## 定义一个agent
# 一个agent最重要的能力是可以使用工具， 因此这里给它配置一个tool。 这里用自定义的tool
weather_agent = Agent(
    role='Weather Reporters',
    goal='Find the highest temperature of Beijing today, and add the number with 100.',
    backstory="""You're a Weather Reporters. You know the weather of the given city, and  you will report the higest temperature.""",
    verbose=True,
    # llm=llm    ### 注意使用方式2时， 这里需要手动传入llm
    tools=[search_tool, my_tool],
)

## 定义任务
task = Task(
    description='Find the highest temperature of Beijing today, and add the number with 100.',
    expected_output='A single number',
    agent=weather_agent,
    tools=[]  ##任务也可以给定一个tool， 只针对这个任务使用特定tools,这里不需要
)

## 任务编配， 其实就是把任务分给相应的agent。 跟团队一起分配任务干活很像。
crew = Crew(
    agents=[weather_agent],
    tasks=[task],
    verbose=2
)

## 调用 kickoff 执行
result = crew.kickoff()
print(result)

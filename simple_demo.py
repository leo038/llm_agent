import os

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

##默认方式，直接使用gpt4, 需要设置OPENAI_API_KEY
# os.environ["OPENAI_API_KEY"] = "Your Key"


os.environ["SERPER_API_KEY"] = "your serper key"  ## 使用SerperDevTool 需要key进行鉴权， 如果没有去官网免费申请一个

# ###通过Ollama使用本地模型的方式1:
os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'  ## 这里如果填http://localhost:11434 会报404错误
os.environ["OPENAI_MODEL_NAME"] = 'qwen2:7b'  # Adjust based on available model
os.environ["OPENAI_API_KEY"] = 'NA'
# ######################################


# ###通过Ollama使用本地模型的方式2:
# from langchain.llms import Ollama
#
# llm = Ollama(
#     model="llama3:8b",)
#     # base_url="http://localhost:11434/")  #
"""#不给base_url参数也可以。 如果给的话这里写http://localhost:11434/v1 会报错，提示langchain_community.llms.ollama.OllamaEndpointNotFoundError:
 Ollama call failed with status code 404. Maybe your model is not found and you should pull the model with `ollama pull llama3:8b`."""
# ##############################

search_tool = SerperDevTool()
## 定义一个agent
# 一个agent最重要的能力是可以使用工具， 因此这里给它配置一个tool。 这个用的是一个搜索工具， 当大模型判断需要联网搜索时， 就可以用这个工具进行搜索。
research_agent = Agent(
    role='Researcher',
    goal='Find and summarize the latest AI news',
    backstory="""You're a researcher at a large company.
  You're responsible for analyzing data and providing insights
  to the business.""",
    verbose=True,
    # llm=llm    ### 注意使用方式2时， 这里需要手动传入llm
    tools=[search_tool],
)

## 定义任务
task = Task(
    description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    agent=research_agent,
    tools=[]  ##任务也可以给定一个tool， 只针对这个任务使用特定tools,这里不需要
)

## 任务编配， 其实就是把任务分给相应的agent。 跟团队一起分配任务干活很像。
crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=2
)

## 调用 kickoff 执行
result = crew.kickoff()
print(result)

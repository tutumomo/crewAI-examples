"""
相比於 demo.py 加入了 human_tools，可以人工介入
如果不指定使用哪一個大模型，預設是使用 chatgpt
"""
import os
from crewai import Agent, Task, Crew, Process
from langchain.agents import load_tools
from langchain.tools import DuckDuckGoSearchRun
# You can choose to use a local model through Ollama for example.
from langchain.llms import Ollama

ollama_llm = Ollama(model="openchat") # 或是 codellama, llama2, llama2-uncensored, llava, mistrak, neural-chat, openchat, openhermes, qwen, starling-lm 
search_tool = DuckDuckGoSearchRun()

# Loading Human Tools，很神奇的東西，可以讓 agent 能够和 human 進行對話。
human_tools = load_tools(["human"])

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science in',
  backstory="""You are a Senior Research Analyst at a leading tech think tank.
  Your expertise lies in identifying emerging trends and technologies in AI and
  data science. You have a knack for dissecting complex data and presenting
  actionable insights. You should reply in traditional chinese.""",
  verbose=True,
  allow_delegation=False,
  # Passing human tools to the agent，加了這個之後，會詢問使用者的意見，怎麼問法？應該是由大模型決定，但添加之後，從沒問過，應該還有問題。
  tools=[search_tool]+human_tools,
  llm=ollama_llm
)
writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a renowned Tech Content Strategist, known for your insightful
  and engaging articles on technology and innovation. With a deep understanding of
  the tech industry, you transform complex concepts into compelling narratives. You should reply in traditional chinese.""",
  verbose=True,
  allow_delegation=True,
  llm=ollama_llm
)

# Create tasks for your agents
# Being explicit on the task to ask for human feedback.
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.
  Compile your findings in a detailed report. 
  Make sure to check with the human if the draft is good before returning your Final Answer.
  Your final answer MUST be a full analysis report in traditional chinese.""",
  agent=researcher
)

task2 = Task(
  description="""Using the insights from the researcher's report, develop an engaging blog
  post that highlights the most significant AI advancements.
  Your post should be informative yet accessible, catering to a tech-savvy audience.
  Aim for a narrative that captures the essence of these breakthroughs and their
  implications for the future. 
  Your final answer MUST be the full blog post of at least 5 paragraphs in traditional chinese using markdown.""",
  agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
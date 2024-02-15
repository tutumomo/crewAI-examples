"""
Demo 01: 
將官方的AI平台crewai，一個最簡單的Agent的執行，
從2個 agents 練習增加一個 翻譯 的 agent(其實本來2個也可以直接讓他輸出繁體中文就好了，不需要再去增加一個翻譯的 Agent，純粹只是拿來練習)
Demo 02: 
1跟2的智能體嘗試調用 ollama 的本地大模型，3的智能體則使用 openAI，來完成 crewai 的多智能體框架執行任務
"""
import os
from crewai import Agent, Task, Crew, Process
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools

# os.environ["OPENAI_API_KEY"]

# You can choose to use a local model through Ollama for example.
#
from langchain.llms import Ollama
# ollama_llm = Ollama(model="openhermes") 
ollama_llm = Ollama(model="mistral") 

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# Loading Human Tools，很神奇的東西，可以讓 agent 能够和 human 進行對話。
human_tools = load_tools(["human"])

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting
  actionable insights.""",
  verbose=True,
  allow_delegation=False,
  # Passing human tools to the agent，加了這個之後，會詢問使用者的意見，怎麼問法？應該是由大模型決定。
  tools=[search_tool]+human_tools ,

  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  llm=ollama_llm # was defined above in the file
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)

writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a renowned Content Strategist, known for
  your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
  verbose=True,
  allow_delegation=True,
  llm=ollama_llm
)
translate= Agent(
  role='professional translator',
  goal='Translate English text content into Traditional Chinese text content',
  backstory="""You are a professional translator with 30 years of working experience. 
  You are good at translating English text into beautiful and smooth Traditional Chinese content.""",
  verbose=True,
  allow_delegation=True,
  llm=ollama_llm
  # llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7) 
)
# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.
  Your final answer MUST be a full analysis report""",
  agent=researcher
)

task2 = Task(
  description="""Using the insights provided, develop an engaging blog
  post that highlights the most significant AI advancements.
  Your post should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI.
  Your final answer MUST be the full blog post of at least 4 paragraphs.""",
  agent=writer
)
task3 = Task(
  description="""Translate the generated full blog post from English to Chinese and output it.""",
  agent=translate
)
# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer, translate],
  tasks=[task1, task2, task3],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
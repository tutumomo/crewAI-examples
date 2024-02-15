import os
from crewai import Agent, Task, Crew, Process
"""
系統環境變數已經有設定 OPENAI_API_KEY，下面的指令根本可以不執行
"""
# os.environ["OPENAI_API_KEY"]

# You can choose to use a local model through Ollama for example.
from langchain.llms import Ollama
ollama_llm = Ollama(model="openhermes") # 或是 mistral, codellama2, llama2
""" 以下是 家裡桌機有下載的大模型, 20240210 推薦使用 mistral
nexusraven 說明文件有強調它函數調用功能強化, 但目前我沒有測試過
llava 是支援多模態的大模型, 但目前我沒有測試過
codellama:latest                8fdf8f752f6e    3.8 GB  7 weeks ago
llama2:latest                   78e26419b446    3.8 GB  2 weeks ago
llama2-uncensored:latest        44040b922233    3.8 GB  10 days ago
llava:latest                    cd3274b81a85    4.5 GB  11 days ago
mistral:latest                  1ab49bc0b6a8    4.1 GB  7 weeks ago
neural-chat:latest              f4c6a8e532e8    4.1 GB  7 weeks ago
nexusraven:latest               483a8282af74    7.4 GB  2 weeks ago
qwen:latest                     d53d04290064    2.3 GB  3 days ago
starling-lm:latest              ff4752739ae4    4.1 GB  7 weeks ago
"""
# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

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
  tools=[search_tool],
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
  # (optional) llm=ollama_llm
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
  Your final answer MUST be the full blog post of at least 4 paragraphs.
  And always use Traditional chinese to express.
  """,
  agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
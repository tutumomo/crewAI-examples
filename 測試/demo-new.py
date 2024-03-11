import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# 設定4個 LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
# crewai 使用 Ollama 的方法：windows 只需要打開 ubuntu 視窗即可，不需要執行 litellm；Mac 則甚至不需要啟動任何程式，只要有安裝好 Ollama 即可調用。
# 與 autogen 不同，autogen 要調用 Ollama 需要執行 litellm，多一道步驟，比較麻煩
gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.7),
# Ollama 大模型，可以看要用哪一個
# ollama = Ollama(model="openhermes_assistant")  # 這是用 modelfile 建立的
# ollama 2024/03/12 最強大模型 nous-hermes2
ollama = Ollama(model="nous-hermes2")

gemini = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.6,
                             google_api_key = os.environ["GOOGLE_API_KEY"]
                             )

# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
# os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key

# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool]
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic or others (https://docs.crewai.com/how-to/LLM-Connections/)
  #
  # import os
  # os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'
  #
  # OR
  #
  # from langchain_openai import ChatOpenAI
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)
writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
  verbose=True,
  allow_delegation=True
)

# 上面建立 agent 時，可以不指定 llm，這裡才指定
researcher.llm = ollama
writer.llm = ollama

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.""",
  expected_output="Full analysis report in bullet points",
  agent=researcher
)

task2 = Task(
  description="""Using the insights provided, develop an engaging blog
  post that highlights the most significant AI advancements.
  Your post should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI.
  Your answer MUST be the full blog post of at least 5 paragraphs and finally using taditional chinese writing.""",
  expected_output="Full blog post of at least 4 paragraphs",
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
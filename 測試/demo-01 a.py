"""
Demo 01: Simple Agent Execution
將官方的AI平台crewai，一個最簡單的Agent的執行，
從2個 agents 再增加一個 翻譯 的 agent
Demo 01a: 加入 human_tools
"""
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI

from langchain.agents import load_tools

# os.environ["OPENAI_API_KEY"]

# You can choose to use a local model through Ollama for example.
# 設定4個 LLM
# crewai 使用 Ollama 的方法：windows 只需要打開 ubuntu 視窗即可，不需要執行 litellm；Mac 則甚至不需要啟動任何程式，只要有安裝好 Ollama 即可調用。
# 與 autogen 不同，autogen 要調用 Ollama 需要執行 litellm，多一道步驟，比較麻煩
gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.7),
# Ollama 大模型，可以看要用哪一個
ollama = Ollama(model="openhermes_assistant")  # 這是用 modelfile 建立的
ollama_openhermes = Ollama(model="openhermes")

gemini = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.6,
                             google_api_key = os.environ["GOOGLE_API_KEY"]
                             )

# 設定工具 tools
# Make sure to Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search
# 最簡易型的工具定義方式
from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# 從 tools 模組中引入需要的工具
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.file_tools import FileTools
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools
# 下面添加 tools 時，必須用 類別.方法 加入工具
# BrowserTools.scrape_and_summarize_website
# CalculatorTools.calculate
# FileTools.write_file
# SearchTools.search_internet、SearchTools.search_news
# SECTools.search_10q、SECTools.search_10k
# 下面的是依樣畫葫蘆自行加入2行定義類別，親測可以匯入
from tools.find_papers_arxiv import FindPapersArxiv
from tools.get_top_hackernews_stories import GetTopHackernewsStories
# 然後就可以用下面的函式來使用工具，已測試可以~~~
# FindPapersArxiv.search_arxiv
# GetTopHackernewsStories.get_top_hackernews_stories

# Loading Human Tools，加了會報錯，正確用法還需要再研究
# human_tools = load_tools(["human"])

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
  # Passing human tools to the agent
  tools= [
          search_tool, 
          BrowserTools.scrape_and_summarize_website, 
          CalculatorTools.calculate, 
          FileTools.write_file,
          SearchTools.search_internet, SearchTools.search_news,
          SECTools.search_10q, SECTools.search_10k,
          FindPapersArxiv.search_arxiv,
          GetTopHackernewsStories.get_top_hackernews_stories
          ]          
          # ] + human_tools,
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  # llm=ollama_llm # was defined above in the file
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
  # llm=ollama_llm
  # (optional) llm=ollama_llm
)

translate= Agent(
  role='professional translator',
  goal='Translate English text content into Traditional Chinese text content',
  backstory="""You are a professional translator with 30 years of working experience. 
  You are good at translating English text into beautiful and smooth Traditional Chinese content.""",
  verbose=True,
  allow_delegation=True,
  # llm=ollama_llm  
  # (optional) llm=ollama_llm  
)

# 上面可以先不指定用哪一個 llm，這裡再指定就可以
researcher.llm = gemini
writer.llm = ollama
translate.llm = gemini

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
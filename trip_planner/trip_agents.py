# Agent 定義，使用 gemini pro 可行。
# 匯入套件
import os
from crewai import Agent
# from langchain.llms import OpenAI
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI

# 設定4個 LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
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

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

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

"""
定義了一個名為 TripAgents 的類別，其中包含了三個方法：
city_selection_agent: 創建一個城市選擇專家的代理人，其目標是根據天氣、季節和價格來選擇最佳城市。
local_expert: 創建一個當地專家的代理人，其目標是提供有關所選城市的最佳見解。
travel_concierge: 創建一個旅行服務的代理人，其目標是創建最令人驚艷的旅行行程，包括預算和打包建議。
"""
class TripAgents():

  def city_selection_agent(self):
    return Agent(
        role='City Selection Expert',
        goal='Select the best city based on weather, season, and prices.',
        backstory=
        'An expert in analyzing travel data to pick ideal destinations',
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        llm = ollama,
        # llm = gemini,
        verbose=True)

  def local_expert(self):
    return Agent(
        role='Local Expert at this city',
        goal='Provide the BEST insights about the selected city.',
        backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        llm = ollama,
        # llm = gemini,
        verbose=True)

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city.""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
            CalculatorTools.calculate,
        ],
        llm = ollama,
        # llm = gemini,
        verbose=True)

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools

from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
# 設定4個 LLM
# crewai 使用 Ollama 的方法：windows 只需要打開 ubuntu 視窗即可，不需要執行 litellm；Mac 則甚至不需要啟動任何程式，只要有安裝好 Ollama 即可調用。
# 與 autogen 不同，autogen 要調用 Ollama 需要執行 litellm，多一道步驟，比較麻煩
""" 
gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.7),
ollama = Ollama(model="openhermes_assistant")  # 這是用 modelfile 建立的
gemini = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.6,
                             google_api_key = os.environ["GOOGLE_API_KEY"]
                             )
"""                    
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
# 下面的是沒有類別，只有定義函式的工具
# from tools.find_papers_arxiv import FindPapersArxiv
# from tools.find_papers_arxiv import *
# from tools.get_top_hackernews_stories import GetTopHackernewsStories
# from tools.get_top_hackernews_stories import *
# FindPapersArxiv.search_arxiv
# GetTopHackernewsStories.get_top_hackernews_stories

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class CustomAgents:
    def __init__(self):
        self.gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.Ollama = Ollama(model="openhermes")
        self.gemini = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.6,
                             google_api_key = os.environ["GOOGLE_API_KEY"]
                             )
    def agent_1(self):
        return Agent(
            role="You are a helpful assistant",
            backstory=dedent(f"""Define agent 1 backstory here"""),
            goal=dedent(f"""Define agent 1 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.gemini,
        )

    def agent_2(self):
        return Agent(
            role="You are a helpful assistant",
            backstory=dedent(f"""Define agent 2 backstory here"""),
            goal=dedent(f"""Define agent 2 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.gemini,
        )

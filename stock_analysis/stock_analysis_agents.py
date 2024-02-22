import os
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
# crewai 使用 Ollama 的方法：原本 windows 需要打開 ubuntu 視窗，20240220 Ollama 發布 windows 版後，就可以不需要 Ubyntu 囉，也不需要執行 litellm；Mac 則甚至不需要啟動任何程式，只要有安裝好 Ollama 即可調用。
# 與 autogen 不同，autogen 要調用 Ollama 需要執行 litellm，多一道步驟，比較麻煩
gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.7),
ollama = Ollama(model="openhermes_assistant")  # 這是用 modelfile 建立的
gemini = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.6,
                             google_api_key = os.environ["GOOGLE_API_KEY"]
                             )

class StockAnalysisAgents():
  def financial_analyst(self):
    return Agent(
      role='The Best Financial Analyst',
      goal="""Impress all customers with your financial data 
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super important customer. You should always reply in English and traditional chinese both.""",
      verbose=True,
      llm = gemini,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )

  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your customer with it""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through news, company announcements, 
      and market sentiments. Now you're working on a super 
      important customer. You should always reply in English and traditional chinese both.""",
      verbose=True,
      llm = gemini,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        YahooFinanceNewsTool(),
        SECTools.search_10q,
        SECTools.search_10k
      ]
  )

  def investment_advisor(self):
    return Agent(
      role='Private Investment Advisor',
      goal="""Impress your customers with full analyses over stocks
      and completer investment recommendations""",
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic investment advice. You are now working for
      a super important customer you need to impress. You should always reply in English and traditional chinese both.""",
      verbose=True,
      llm = gemini,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate,
        YahooFinanceNewsTool(),
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )
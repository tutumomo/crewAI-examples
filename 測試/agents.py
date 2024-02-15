"""
這個案例用的是 "instagram_post" 的 agents.py
原本使用 ollamaa 這個本地大模型
增加各個 LLM 的設定，可以使用不同的 LLM 來生成不同的結果
"""
# 導入需要的模組
import os
from textwrap import dedent
from crewai import Agent
from langchain.agents import load_tools
# 導入本地自訂的 tools 庫
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools

"""
可以使用 default_llm = Ollama() 來定義 default_llm
也可以定義好幾個不同的 llm 讓各個 Agent 使用
當 agent 設定時，可以指定 llm，如果 agent 沒有指定 llm，則使用 default_llm，default_llm 未設定時，預設就是使用 OpenAI 的 llm。

"""
from langchain_google_genai import ChatGoogleGenerativeAI
llm_1 = ChatGoogleGenerativeAI(
    model = "gemini-pro",
    verbose = True,
    temperature = 0.6,
    google_api_key = os.environ["GOOGLE_API_KEY"]
    )

from langchain.llms import Ollama
# llm_2 = Ollama(model=os.environ['MODEL'])
# llm_2 = Ollama(model="openhermes") 
llm_2 = Ollama(model="mistral") 

from langchain_openai import AzureChatOpenAI
llm_3 = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)
# 上面設定好各種 llm 之後，下面就可以設定 default_llm 的開關，如果不設定，就是使用 OpenAI 的 llm
default_llm = llm_1

# 以下是原參考檔設定的 Agent
class MarketingAnalysisAgents:
	def __init__(self):
		# self.llm = Ollama(model=os.environ['MODEL'])
		self.llm = default_llm
	def product_competitor_agent(self):
		return Agent(
			role="Lead Market Analyst",
			goal=dedent("""\
				Conduct amazing analysis of the products and
				competitors, providing in-depth insights to guide
				marketing strategies."""),
			backstory=dedent("""\
				As the Lead Market Analyst at a premier
				digital marketing firm, you specialize in dissecting
				online business landscapes."""),
			tools=[
					BrowserTools.scrape_and_summarize_website,
					SearchTools.search_internet
			],
			allow_delegation=False,
			llm=self.llm,
			verbose=True
		)

	def strategy_planner_agent(self):
		return Agent(
			role="Chief Marketing Strategist",
			goal=dedent("""\
				Synthesize amazing insights from product analysis
				to formulate incredible marketing strategies."""),
			backstory=dedent("""\
				You are the Chief Marketing Strategist at
				a leading digital marketing agency, known for crafting
				bespoke strategies that drive success."""),
			tools=[
					BrowserTools.scrape_and_summarize_website,
					SearchTools.search_internet,
					SearchTools.search_instagram
			],
			llm=self.llm,
			verbose=True
		)

	def creative_content_creator_agent(self):
		return Agent(
			role="Creative Content Creator",
			goal=dedent("""\
				Develop compelling and innovative content
				for social media campaigns, with a focus on creating
				high-impact Instagram ad copies."""),
			backstory=dedent("""\
				As a Creative Content Creator at a top-tier
				digital marketing agency, you excel in crafting narratives
				that resonate with audiences on social media.
				Your expertise lies in turning marketing strategies
				into engaging stories and visual content that capture
				attention and inspire action."""),
			tools=[
					BrowserTools.scrape_and_summarize_website,
					SearchTools.search_internet,
					SearchTools.search_instagram
			],
			llm=self.llm,
			verbose=True
		)

	def senior_photographer_agent(self):
		return Agent(
				role="Senior Photographer",
				goal=dedent("""\
					Take the most amazing photographs for instagram ads that
					capture emotions and convey a compelling message."""),
				backstory=dedent("""\
					As a Senior Photographer at a leading digital marketing
					agency, you are an expert at taking amazing photographs that
					inspire and engage, you're now working on a new campaign for a super
					important customer and you need to take the most amazing photograph."""),
				tools=[
					BrowserTools.scrape_and_summarize_website,
					SearchTools.search_internet,
					SearchTools.search_instagram
				],
				llm=self.llm,
				allow_delegation=False,
				verbose=True
		)

	def chief_creative_diretor_agent(self):
		return Agent(
				role="Chief Creative Director",
				goal=dedent("""\
					Oversee the work done by your team to make sure it's the best
					possible and aligned with the product's goals, review, approve,
					ask clarifying question or delegate follow up work if necessary to make
					decisions"""),
				backstory=dedent("""\
					You're the Chief Content Officer of leading digital
					marketing specialized in product branding. You're working on a new
					customer, trying to make sure your team is crafting the best possible
					content for the customer."""),
				tools=[
					BrowserTools.scrape_and_summarize_website,
					SearchTools.search_internet,
					SearchTools.search_instagram
				],
				llm=self.llm,
				verbose=True
		)

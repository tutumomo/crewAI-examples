# 匯入套件
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process

# 匯入工具
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.file_tools import FileTools
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools
from tools.template_tools import TemplateTools
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool

gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.7),
ollama_llm = Ollama(model="openhermes"),
# gemini 突然變成無法執行了，哀
gemini = ChatGoogleGenerativeAI(model = "gemini-pro", verbose = True, temperature = 0.6, google_api_key = os.environ["GOOGLE_API_KEY"]),

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
"""
tools=[
    search_DuckDuck,
    BrowserTools.scrape_and_summarize_website,
    CalculatorTools.calculate,
    FileTools.write_file,     
    SearchTools.search_internet,
    SearchTools.search_news,
    SECTools.search_10q,
    SECTools.search_10k,
    TemplateTools.learn_landing_page_options,
    TemplateTools.copy_landing_page_template_to_project_folder,
    YahooFinanceNewsTool()
    ]
"""

researcher = Agent(role = 'Senior Research Analyst', goal = 'Uncover cutting-edge development in AI and data science', backstory = """ You work in a leading tech think tank. Your expertise lies in identifying emerging trends. You have a knack for dissecting complex data and presenting actionable insights.""", verbose=True, allow_delegation=False, llm = ollama_llm)
writer = Agent(role='Tech Content Strategist', goal='Craft compelling content on tech advancements', backstory=""" You are a renowned Content Strategist, known for your insightful and engaging articles. You transform complex concepts into compelling narratives. And you are expert at writing in traditional chinese. """, verbose=True, allow_delegation=True, llm = ollama_llm)
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
  Your final answer MUST be the full blog post of at least 5 paragraphs.
  And always use Traditional chinese to express.
  """,
  agent=writer
)

crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

result = crew.kickoff()

print("######################")
print(result)
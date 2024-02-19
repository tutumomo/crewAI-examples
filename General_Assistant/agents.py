# 匯入套件
import os
from crewai import Agent
from textwrap import dedent
from langchain_community.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# 匯入工具
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.file_tools import FileTools
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools
from tools.template_tools import TemplateTools

from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool


# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
# agent_1_name、agent_2_name 的名稱就不改了，因為 main.py 會用到，但 role、backstory、goal、tools 都可以改

class CustomAgents:
    def __init__(self):
        self.GPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
        self.GPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7),
        self.Ollama = Ollama(model="openhermes"),
        self.Gemini_llm = ChatGoogleGenerativeAI(model = "gemini-pro", verbose = True, temperature = 0.6, google_api_key = os.environ["GOOGLE_API_KEY"]),
        self.llm=self.Gemini_llm

    def agent_1_name(self):
        return Agent(
            role="A user proxy agent that executes code.",
            backstory=dedent(f"""You are a helpful assistant. You should always respond in Traditional Chinese. 一旦使用者的要求達成，應即刻停止對話，並即刻輸出結果。"""),
            goal=dedent(f"""You are a helpful assistant. 須盡力解決並達成使用者的要求，並給出滿意的答覆。"""),
            tools=[
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
                ],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    def agent_2_name(self):
        return Agent(
            role="A primary assistant agent that writes plans and code to solve tasks.",
            backstory=dedent(f"""You are a helpful AI assistant. Solve tasks using your coding and language skills. In the following cases, suggest python code (in a python coding block) or shell script (in a cmd coding block) for the user to execute. 1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself. 2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly. Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill. When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user. If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user. If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try. When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible. Reply 'TERMINATE' in the end when everything is done. 全部過程包含中間過程對話、程式註解及最後結果均使用繁體中文。"""),
            goal=dedent(f"""writes plans and code to solve tasks."""),
            tools=[
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
                ],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

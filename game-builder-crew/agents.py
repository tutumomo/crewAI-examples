"""
改成調用免費的gemini pro，加入下列指令
import os
from langchain_google_genai import ChatGoogleGenerativeAI
Gemini_llm = ChatGoogleGenerativeAI(
    model = "gemini-pro",
    verbose = True,
    temperature = 0.6,
    google_api_key = os.environ["GOOGLE_API_KEY"]
    )

class 定義的 agent 裡面加入
llm = Gemini_llm
=============================================
加入可以寫入檔案的 tools
"""
# 匯入套件
import os
from textwrap import dedent
from crewai import Agent
from langchain.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# 匯入 tools
from tools.file_tools import FileTools

# 建立 LLMs
GPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
GPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
Ollama = Ollama(model="openhermes")
Ollama_openhermes = Ollama(model="openhermes_assistant")
Gemini = ChatGoogleGenerativeAI(model = "gemini-pro",verbose = True,temperature = 0.6,google_api_key = os.environ["GOOGLE_API_KEY"])
llm = Ollama_openhermes # 在這裡指定要使用上面的哪一個大模型即可

class GameAgents():
	def senior_engineer_agent(self):
		return Agent(
			role='Senior Software Engineer',
			goal='Create software as needed',
			backstory=dedent("""\
				You are a Senior Software Engineer at a leading tech think tank.
				Your expertise in programming in python. and do your best to
				produce perfect code"""),
			allow_delegation=False,
			llm = llm,
			tools = [FileTools.write_file], 
			verbose=True
		)

	def qa_engineer_agent(self):
		return Agent(
			role='Software Quality Control Engineer',
  			goal='create prefect code, by analizing the code that is given for errors',
  			backstory=dedent("""\
				You are a software engineer that specializes in checking code
  			for errors. You have an eye for detail and a knack for finding
				hidden bugs.
  			You check for missing imports, variable declarations, mismatched
				brackets and syntax errors.
  			You also check for security vulnerabilities, and logic errors"""),
			allow_delegation=False,
			tools = [FileTools.write_file], 
			llm = llm,
			verbose=True
		)

	def chief_qa_engineer_agent(self):
		return Agent(
			role='Chief Software Quality Control Engineer',
  			goal='Ensure that the code does the job that it is supposed to do',
  			backstory=dedent("""\
				You feel that programmers always do only half the job, so you are
				super dedicate to make high quality code."""),
			allow_delegation=True,
			tools = [FileTools.write_file], 
			llm = llm,
			verbose=True
		)
crewAI 範例的基本架構，
主程式：main.py
智能體：agent.py
任務：task.py
另外，調用的函數會放在 Tools 資料夾內。

想使用非 OpenAI 的大模型，必須修改 Agent.py。
crewAI 預設使用 OpenAI 大模型，也可以使用 Ollama(本地)、Gemini Pro 的大模型，使用法如下：
方法1. 同時列入 Ollama、Gemini Pro，使用時再擇一
import os
from langchain.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI

Ollama_llm = Ollama(model="openhermes")

Gemini_llm = ChatGoogleGenerativeAI(
    model = "gemini-pro",
    verbose = True,
    temperature = 0.6,
    google_api_key = os.environ["GOOGLE_API_KEY"]
    )

class 定義的 agent 裡面加入
llm = Ollama_llm # 或是
llm = Gemini_llm

方法2. 列出 GPT3.5、GPT4、Ollama、Gemini Pro，使用時再擇一即可。
from langchain_google_genai import ChatGoogleGenerativeAI

# This is an example of how to define custom agents.

# You can define as many agents as you want.

# You can also define custom tasks in tasks.py

class CustomAgents:
    def __init__(self):
        self.GPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.GPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.Ollama = Ollama(model="openhermes")
        self.Gemini_llm = ChatGoogleGenerativeAI(model = "gemini-pro", verbose = True, temperature = 0.6, google_api_key = os.environ["GOOGLE_API_KEY"])

    def agent_1_name(self):
        return Agent(
            role="Define agent 1 role here",
            backstory=dedent(f"""Define agent 1 backstory here"""),
            goal=dedent(f"""Define agent 1 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            # llm=self.OpenAIGPT35,
            # llm=self.Ollama,
            llm=self.Gemini_llm,
        )

    def agent_2_name(self):
        return Agent(
            role="Define agent 2 role here",
            backstory=dedent(f"""Define agent 2 backstory here"""),
            goal=dedent(f"""Define agent 2 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            # llm=self.OpenAIGPT35,
            # llm=self.Ollama,
            llm=self.Gemini_llm,
        )

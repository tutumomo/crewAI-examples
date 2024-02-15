# 用 CrewAI Assistant 幫忙產出的 CrewAI Chatbot，但似乎不可行，無法持續聊天對話。
from crewai import Agent, Task, Crew, Process
from langchain.chat_models import ChatOpenAI

# 定義一個代理：聊天機器人，能夠進行持續對話
chatbot_agent = Agent(
    role='Chatbot',
    goal='Engage in a continuous and coherent conversation in Traditional Chinese',
    backstory='A chatbot trained to converse fluently in Traditional Chinese on a wide range of topics.',
    verbose=True,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),  # 使用特定的語言模型，例如 GPT-3.5 Turbo，確保支持繁體中文
    allow_delegation=False  # 確保代理不會將任務委派給其他代理
)

# 創建一個任務：持續的繁體中文對話
chatbot_task = Task(
    description='Engage in a continuous and coherent conversation with the user in Traditional Chinese.',
    agent=chatbot_agent
)

# 組建一個團隊：包含聊天機器人的團隊
chatbot_crew = Crew(
    agents=[chatbot_agent],
    tasks=[chatbot_task],
    process=Process.sequential,  # 任務將依序執行
    verbose=True
)

# 啟動團隊，讓聊天機器人開始工作
result = chatbot_crew.kickoff()

# 輸出結果
print(result)
